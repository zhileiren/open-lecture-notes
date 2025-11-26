// FixedReturnPass.cpp
// LLVM 18, New PM plugin: For integer-returning functions, replace each 'ret'
// with a constant '1' of the correct integer bitwidth.

#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct BuggyReturnPass : public PassInfoMixin<BuggyReturnPass> {
  PreservedAnalyses run(Module &M, ModuleAnalysisManager &) {
    LLVMContext &C = M.getContext();

    for (Function &F : M) {
      if (F.isDeclaration()) continue;

      Type *retTy = F.getReturnType();
      // only target integer return types
      if (!retTy->isIntegerTy()) continue;

      IntegerType *IT = cast<IntegerType>(retTy);
      unsigned bitWidth = IT->getBitWidth();

      // Build the constant of the *correct* width
      Constant *oneConst = ConstantInt::get(IT, 1);

      for (BasicBlock &BB : F) {
        // iterate carefully since we erase instructions
        for (auto it = BB.begin(); it != BB.end(); ) {
          Instruction &I = *it++;
          if (ReturnInst *RI = dyn_cast<ReturnInst>(&I)) {
            // If the return is void (no operand) this won't run because we
            // already checked F returns an integer type.
            // Insert new return with correct typed constant
            IRBuilder<> B(RI);
            B.CreateRet(oneConst);
            RI->eraseFromParent();
          }
        }
      }
    }

    return PreservedAnalyses::none();
  }
};

} // anonymous namespace

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return {
    LLVM_PLUGIN_API_VERSION,
    "BuggyReturnPass",
    LLVM_VERSION_STRING,
    [](PassBuilder &PB) {
      // Register so it can be used via -passes=name
      PB.registerPipelineParsingCallback(
        [](StringRef Name, ModulePassManager &MPM, ArrayRef<PassBuilder::PipelineElement>) {
          if (Name == "buggy-return-pass") {
            MPM.addPass(BuggyReturnPass());
            return true;
          }
          return false;
        });

      // Also automatically insert at pipeline start so clang can run it without -mllvm -passes
      PB.registerPipelineStartEPCallback(
        [](ModulePassManager &MPM, OptimizationLevel) {
          MPM.addPass(BuggyReturnPass());
        });
    }
  };
}

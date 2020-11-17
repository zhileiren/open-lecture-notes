#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

who_data = pd.read_csv("WHO-COVID-19-global-data.csv", parse_dates=[0])
# strip the white space in the header
who_data.columns = [col.strip() for col in who_data.columns]

us = who_data[who_data['Country_code'] == 'US']
cn = who_data[who_data['Country_code'] == 'CN']
gb = who_data[who_data['Country_code'] == 'GB']

print(us.head())
print(cn.tail())

us.plot(x='Date_reported', y='New_cases', kind='line')
plt.savefig("us_new_cases.png")
cn.plot(x='Date_reported', y='New_cases', kind='line')
plt.savefig("cn_new_cases.png")

merged = pd.merge(us, gb, on="Date_reported", suffixes=("_US", "_GB"))
print(merged.head())
merged.plot(x="New_cases_US", y="New_cases_GB", kind="scatter")
plt.savefig("merged.png")


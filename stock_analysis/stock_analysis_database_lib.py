import json
import os
import sys
import boto3
import sqlite3
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from pathlib import Path

## database
stock_ticker_data=[ 
    # {
    #     "symbol" : "PRAA",
    #     "name" : "PRA Group, Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "AMZN",
    #     "name" : "Amazon.com, Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "TSLA",
    #     "name" : "Tesla Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "PAAS",
    #     "name" : "Pan American Silver Corp.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "PAAC",
    #     "name" : "Proficient Alpha Acquisition Corp.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqCM",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "RYAAY",
    #     "name" : "Ryanair Holdings plc",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "MPAA",
    #     "name" : "Motorcar Parts of America, Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "STAA",
    #     "name" : "STAAR Surgical Company",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGM",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "RBCAA",
    #     "name" : "Republic Bancorp, Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "AABA",
    #     "name" : "Altaba Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGS",
    #     "exchangeShortName" : "NASDAQ"    
    # }, 
    # {
    #     "symbol" : "AAXJ",
    #     "name" : "iShares MSCI All Country Asia ex Japan ETF",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGM",
    #     "exchangeShortName" : "NASDAQ"
    # }, 
    # {
    #     "symbol" : "ZNWAA",
    #     "name" : "Zion Oil & Gas, Inc.",
    #     "currency" : "USD",
    #     "stockExchange" : "NasdaqGM",
    #     "exchangeShortName" : "NASDAQ"
    # },
    {
  "symbol": "AACG",
  "name": "ATA Creativity Global ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AACI",
  "name": "Armada Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AACIU",
  "name": "Armada Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AACIW",
  "name": "Armada Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AADI",
  "name": "Aadi Bioscience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AADR",
  "name": "AdvisorShares Dorsey Wright ADR ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAGR",
  "name": "African Agriculture Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAGRW",
  "name": "African Agriculture Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAL",
  "name": "American Airlines Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAME",
  "name": "Atlantic American Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAOI",
  "name": "Applied Optoelectronics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAON",
  "name": "AAON, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAPB",
  "name": "GraniteShares 2x Long AAPL Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAPD",
  "name": "Direxion Daily AAPL Bear 1X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAPU",
  "name": "Direxion Daily AAPL Bull 2X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AAXJ",
  "name": "iShares MSCI All Country Asia ex Japan ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABAT",
  "name": "American Battery Technology Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABCB",
  "name": "Ameris Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABCL",
  "name": "AbCellera Biologics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABCS",
  "name": "Alpha Blue Capital US Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABEO",
  "name": "Abeona Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABIO",
  "name": "ARCA biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABL",
  "name": "Abacus Life, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABLLL",
  "name": "Abacus Life, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABLLW",
  "name": "Abacus Life, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABLV",
  "name": "Able View Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABLVW",
  "name": "Able View Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABNB",
  "name": "Airbnb, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABOS",
  "name": "Acumen Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABSI",
  "name": "Absci Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABTS",
  "name": "Abits Group Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABUS",
  "name": "Arbutus Biopharma Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABVC",
  "name": "ABVC BioPharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ABVX",
  "name": "Abivax SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACAB",
  "name": "Atlantic Coastal Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACABU",
  "name": "Atlantic Coastal Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACABW",
  "name": "Atlantic Coastal Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACAC",
  "name": "Acri Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACACU",
  "name": "Acri Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACACW",
  "name": "Acri Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACAD",
  "name": "ACADIA Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACB",
  "name": "Aurora Cannabis Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACBA",
  "name": "Ace Global Business Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACBAU",
  "name": "Ace Global Business Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACBAW",
  "name": "Ace Global Business Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACCD",
  "name": "Accolade, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACDC",
  "name": "ProFrac Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACET",
  "name": "Adicet Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACGL",
  "name": "Arch Capital Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACGLN",
  "name": "Arch Capital Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACGLO",
  "name": "Arch Capital Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACHC",
  "name": "Acadia Healthcare Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACHL",
  "name": "Achilles Therapeutics plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACHV",
  "name": "Achieve Life Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACIC",
  "name": "American Coastal Insurance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACIU",
  "name": "AC Immune SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACIW",
  "name": "ACI Worldwide, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACLS",
  "name": "Axcelis Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACLX",
  "name": "Arcellx, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACMR",
  "name": "ACM Research, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACNB",
  "name": "ACNB Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACNT",
  "name": "Ascent Industries Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACON",
  "name": "Aclarion, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACONW",
  "name": "Aclarion, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACRS",
  "name": "Aclaris Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACRV",
  "name": "Acrivon Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACST",
  "name": "Acasti Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACT",
  "name": "Enact Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACTG",
  "name": "Acacia Research Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACVA",
  "name": "ACV Auctions Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACWI",
  "name": "iShares MSCI ACWI ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACWX",
  "name": "iShares MSCI ACWI ex U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ACXP",
  "name": "Acurx Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADAG",
  "name": "Adagene Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADAP",
  "name": "Adaptimmune Therapeutics plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADBE",
  "name": "Adobe Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADD",
  "name": "Color Star Technology Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADEA",
  "name": "Adeia Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADI",
  "name": "Analog Devices, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADIL",
  "name": "Adial Pharmaceuticals, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADMA",
  "name": "ADMA Biologics Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADN",
  "name": "Advent Technologies Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADNWW",
  "name": "Advent Technologies Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADP",
  "name": "Automatic Data Processing, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADPT",
  "name": "Adaptive Biotechnologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADSE",
  "name": "ADS",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADSEW",
  "name": "ADS",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADSK",
  "name": "Autodesk, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADTH",
  "name": "AdTheorent Holding Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADTHW",
  "name": "AdTheorent Holding Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADTN",
  "name": "ADTRAN Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADTX",
  "name": "Aditxt, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADUS",
  "name": "Addus HomeCare Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADV",
  "name": "Advantage Solutions Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADVM",
  "name": "Adverum Biotechnologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADVWW",
  "name": "Advantage Solutions Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ADXN",
  "name": "Addex Therapeutics Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEAE",
  "name": "AltEnergy Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEAEU",
  "name": "AltEnergy Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEAEW",
  "name": "AltEnergy Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEHL",
  "name": "Antelope Enterprise Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEHR",
  "name": "Aehr Test Systems ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEI",
  "name": "Alset Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEIS",
  "name": "Advanced Energy Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEMD",
  "name": "Aethlon Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AENT",
  "name": "Alliance Entertainment Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AENTW",
  "name": "Alliance Entertainment Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEP",
  "name": "American Electric Power Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AERT",
  "name": "Aeries Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AERTW",
  "name": "Aeries Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEYE",
  "name": "AudioEye, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AEZS",
  "name": "Aeterna Zentaris Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFAR",
  "name": "Aura FAT Projects Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFARU",
  "name": "Aura FAT Projects Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFARW",
  "name": "Aura FAT Projects Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFBI",
  "name": "Affinity Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFCG",
  "name": "AFC Gamma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFJK",
  "name": "Aimei Health Technology Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFJKR",
  "name": "Aimei Health Technology Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFJKU",
  "name": "Aimei Health Technology Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFMD",
  "name": "Affimed N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFRI",
  "name": "Forafric Global PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFRIW",
  "name": "Forafric Global PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFRM",
  "name": "Affirm Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AFYA",
  "name": "Afya Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGAE",
  "name": "Allied Gaming & Entertainment Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGBA",
  "name": "AGBA Group Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGBAW",
  "name": "AGBA Group Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGEN",
  "name": "Agenus Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGFY",
  "name": "Agrify Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGIO",
  "name": "Agios Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGMH",
  "name": "AGM Group Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGMI",
  "name": "Themes Silver Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNC",
  "name": "AGNC Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNCL",
  "name": "AGNC Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNCM",
  "name": "AGNC Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNCN",
  "name": "AGNC Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNCO",
  "name": "AGNC Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNCP",
  "name": "AGNC Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGNG",
  "name": "Global X Aging Population ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGRI",
  "name": "AgriFORCE  Growing Systems Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGRIW",
  "name": "AgriFORCE  Growing Systems Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGYS",
  "name": "Agilysys, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AGZD",
  "name": "WisdomTree Interest Rate Hedged U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AHCO",
  "name": "AdaptHealth Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AHG",
  "name": "Akso Health Group ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AHI",
  "name": "Advanced Health Intelligence Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIA",
  "name": "iShares Asia 50 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIH",
  "name": "Aesthetic Medical International Holdings Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIHS",
  "name": "Senmiao Technology Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AILE",
  "name": "iLearningEngines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AILEW",
  "name": "iLearningEngines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIMAU",
  "name": "Aimfinity Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIMAW",
  "name": "Aimfinity Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIMBU",
  "name": "Aimfinity Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIMD",
  "name": "Ainos, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIMDW",
  "name": "Ainos, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIP",
  "name": "Arteris, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIQ",
  "name": "Global X Artificial Intelligence & Technology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRE",
  "name": "reAlpha Tech Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRG",
  "name": "Airgain, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRJ",
  "name": "Montana Technologies Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRJW",
  "name": "Montana Technologies Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRL",
  "name": "Themes Airlines ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRR",
  "name": "First Trust RBA American Industrial Renaissance ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRS",
  "name": "AirSculpt Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRT",
  "name": "Air T, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIRTP",
  "name": "Air T, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AISP",
  "name": "Airship AI Holdings, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AISPW",
  "name": "Airship AI Holdings, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AITR",
  "name": "AI TRANSPORTATION ACQUISITION CORP ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AITRR",
  "name": "AI TRANSPORTATION ACQUISITION CORP ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AITRU",
  "name": "AI TRANSPORTATION ACQUISITION CORP ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AIXI",
  "name": "XIAO",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKAM",
  "name": "Akamai Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKAN",
  "name": "Akanda Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKBA",
  "name": "Akebia Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKLI",
  "name": "Akili, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKRO",
  "name": "Akero Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKTS",
  "name": "Akoustis Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKTX",
  "name": "Akari Therapeutics Plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AKYA",
  "name": "Akoya BioSciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALAB",
  "name": "Astera Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALAR",
  "name": "Alarum Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALBT",
  "name": "Avalon GloboCare Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALCE",
  "name": "Alternus Clean Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALCO",
  "name": "Alico, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALCY",
  "name": "Alchemy Investments Acquisition Corp 1 ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALCYU",
  "name": "Alchemy Investments Acquisition Corp 1 ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALCYW",
  "name": "Alchemy Investments Acquisition Corp 1 ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALDX",
  "name": "Aldeyra Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALEC",
  "name": "Alector, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALGM",
  "name": "Allegro MicroSystems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALGN",
  "name": "Align Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALGS",
  "name": "Aligos Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALGT",
  "name": "Allegiant Travel Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALHC",
  "name": "Alignment Healthcare, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALIM",
  "name": "Alimera Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALKS",
  "name": "Alkermes plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALKT",
  "name": "Alkami Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALLK",
  "name": "Allakos Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALLO",
  "name": "Allogene Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALLR",
  "name": "Allarity Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALLT",
  "name": "Allot Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALNT",
  "name": "Allient Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALNY",
  "name": "Alnylam Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALOT",
  "name": "AstroNova, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALPN",
  "name": "Alpine Immune Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALPP",
  "name": "Alpine 4 Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALRM",
  "name": "Alarm.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALRN",
  "name": "Aileron Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALRS",
  "name": "Alerus Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALSA",
  "name": "Alpha Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALSAR",
  "name": "Alpha Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALSAU",
  "name": "Alpha Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALSAW",
  "name": "Alpha Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALT",
  "name": "Altimmune, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALTI",
  "name": "AlTi Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALTO",
  "name": "Alto Ingredients, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALTR",
  "name": "Altair Engineering Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALTY",
  "name": "Global X Alternative Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALVO",
  "name": "Alvotech ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALVOW",
  "name": "Alvotech ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALVR",
  "name": "AlloVir, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALXO",
  "name": "ALX Oncology Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ALZN",
  "name": "Alzamend Neuro, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMAL",
  "name": "Amalgamated Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMAT",
  "name": "Applied Materials, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMBA",
  "name": "Ambarella, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMCX",
  "name": "AMC Networks Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMD",
  "name": "Advanced Micro Devices, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMDL",
  "name": "GraniteShares 2x Long AMD Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMDS",
  "name": "GraniteShares 1x Short AMD Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMED",
  "name": "Amedisys Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMGN",
  "name": "Amgen Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMID",
  "name": "Argent Mid Cap ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMIX",
  "name": "Autonomix Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMKR",
  "name": "Amkor Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMLI",
  "name": "American Lithium Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMLX",
  "name": "Amylyx Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMPG",
  "name": "Amplitech Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMPGW",
  "name": "Amplitech Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMPH",
  "name": "Amphastar Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMPL",
  "name": "Amplitude, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMRK",
  "name": "A",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMRN",
  "name": "Amarin Corporation plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMRX",
  "name": "Amneal Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMSC",
  "name": "American Superconductor Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMSF",
  "name": "AMERISAFE, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMST",
  "name": "Amesite Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMSWA",
  "name": "American Software, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMTX",
  "name": "Aemetis, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMWD",
  "name": "American Woodmark Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMZD",
  "name": "Direxion Daily AMZN Bear 1X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMZN",
  "name": "Amazon.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMZU",
  "name": "Direxion Daily AMZN Bull 2X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AMZZ",
  "name": "GraniteShares 2x Long AMZN Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANAB",
  "name": "AnaptysBio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANDE",
  "name": "The Andersons, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANEB",
  "name": "Anebulo Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANGH",
  "name": "Anghami Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANGHW",
  "name": "Anghami Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANGI",
  "name": "Angi Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANGL",
  "name": "VanEck Fallen Angel High Yield Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANGO",
  "name": "AngioDynamics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANIK",
  "name": "Anika Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANIP",
  "name": "ANI Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANIX",
  "name": "Anixa Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANL",
  "name": "Adlai Nortye Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANNX",
  "name": "Annexon, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANSC",
  "name": "Agriculture & Natural Solutions Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANSCU",
  "name": "Agriculture & Natural Solutions Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANSCW",
  "name": "Agriculture & Natural Solutions Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANSS",
  "name": "ANSYS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANTE",
  "name": "AirNet Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANTX",
  "name": "AN2 Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ANY",
  "name": "Sphere 3D Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AOGO",
  "name": "Arogo Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AOGOU",
  "name": "Arogo Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AOGOW",
  "name": "Arogo Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AONC",
  "name": "American Oncology Network, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AONCW",
  "name": "American Oncology Network, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AOSL",
  "name": "Alpha and Omega Semiconductor Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AOTG",
  "name": "AOT Growth and Innovation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AOUT",
  "name": "American Outdoor Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APA",
  "name": "APA Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APCX",
  "name": "AppTech Payments Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APCXW",
  "name": "AppTech Payments Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APDN",
  "name": "Applied DNA Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APEI",
  "name": "American Public Education, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APGE",
  "name": "Apogee Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "API",
  "name": "Agora, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APLD",
  "name": "Applied Digital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APLM",
  "name": "Apollomics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APLMW",
  "name": "Apollomics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APLS",
  "name": "Apellis Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APLT",
  "name": "Applied Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APM",
  "name": "Aptorum Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APOG",
  "name": "Apogee Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APP",
  "name": "Applovin Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APPF",
  "name": "AppFolio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APPN",
  "name": "Appian Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APPS",
  "name": "Digital Turbine, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APRE",
  "name": "Aprea Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APTO",
  "name": "Aptose Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APVO",
  "name": "Aptevo Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APWC",
  "name": "Asia Pacific Wire & Cable Corporation Limited  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APXI",
  "name": "APx Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APXIU",
  "name": "APx Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APXIW",
  "name": "APx Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "APYX",
  "name": "Apyx Medical Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQB",
  "name": "AquaBounty Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQMS",
  "name": "Aqua Metals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQST",
  "name": "Aquestive Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQU",
  "name": "Aquaron Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQUNR",
  "name": "Aquaron Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQUNU",
  "name": "Aquaron Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AQWA",
  "name": "Global X Clean Water ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARAY",
  "name": "Accuray Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARBB",
  "name": "ARB IOT Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARBE",
  "name": "Arbe Robotics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARBEW",
  "name": "Arbe Robotics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARBK",
  "name": "Argo Blockchain plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARBKL",
  "name": "Argo Blockchain plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARCB",
  "name": "ArcBest Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARCC",
  "name": "Ares Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARCT",
  "name": "Arcturus Therapeutics Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARDX",
  "name": "Ardelyx, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AREB",
  "name": "American Rebel Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AREBW",
  "name": "American Rebel Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AREC",
  "name": "American Resources Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARGX",
  "name": "argenx SE ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARHS",
  "name": "Arhaus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARKO",
  "name": "ARKO Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARKOW",
  "name": "ARKO Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARKR",
  "name": "Ark Restaurants Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARLP",
  "name": "Alliance Resource Partners, L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARM",
  "name": "Arm Holdings plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AROW",
  "name": "Arrow Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARQ",
  "name": "Arq, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARQQ",
  "name": "Arqit Quantum Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARQQW",
  "name": "Arqit Quantum Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARQT",
  "name": "Arcutis Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARRY",
  "name": "Array Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARTL",
  "name": "Artelo Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARTLW",
  "name": "Artelo Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARTNA",
  "name": "Artesian Resources Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARTW",
  "name": "Art's",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARVN",
  "name": "Arvinas, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARVR",
  "name": "First Trust Indxx Metaverse ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARWR",
  "name": "Arrowhead Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ARYD",
  "name": "ARYA Sciences Acquisition Corp IV ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASCB",
  "name": "A SPAC II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASCBR",
  "name": "A SPAC II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASCBU",
  "name": "A SPAC II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASCBW",
  "name": "A SPAC II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASET",
  "name": "FlexShares Real Assets Allocation Index Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASLE",
  "name": "AerSale Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASLN",
  "name": "ASLAN Pharmaceuticals Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASMB",
  "name": "Assembly Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASML",
  "name": "ASML Holding N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASND",
  "name": "Ascendis Pharma A\/S ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASNS",
  "name": "Actelis Networks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASO",
  "name": "Academy Sports and Outdoors, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASPI",
  "name": "ASP Isotopes Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASPS",
  "name": "Altisource Portfolio Solutions S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASRT",
  "name": "Assertio Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASRV",
  "name": "AmeriServ Financial Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASST",
  "name": "Asset Entities Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTC",
  "name": "Astrotech Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTE",
  "name": "Astec Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTH",
  "name": "Astrana Health Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTI",
  "name": "Ascent Solar Technologies, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTL",
  "name": "Algoma Steel Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTLW",
  "name": "Algoma Steel Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTR",
  "name": "Astra Space, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTS",
  "name": "AST SpaceMobile, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASTSW",
  "name": "AST SpaceMobile, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASUR",
  "name": "Asure Software Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ASYS",
  "name": "Amtech Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATAI",
  "name": "ATAI Life Sciences N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATAT",
  "name": "Atour Lifestyle Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATCOL",
  "name": "Atlas Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATEC",
  "name": "Alphatec Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATER",
  "name": "Aterian, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATEX",
  "name": "Anterix Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATGL",
  "name": "Alpha Technology Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATHA",
  "name": "Athira Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATHE",
  "name": "Alterity Therapeutics Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATIF",
  "name": "ATIF Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATLC",
  "name": "Atlanticus Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATLCL",
  "name": "Atlanticus Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATLCP",
  "name": "Atlanticus Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATLCZ",
  "name": "Atlanticus Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATLO",
  "name": "Ames National Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATLX",
  "name": "Atlas Lithium Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMC",
  "name": "AlphaTime Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMCR",
  "name": "AlphaTime Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMCU",
  "name": "AlphaTime Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMCW",
  "name": "AlphaTime Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMV",
  "name": "AlphaVest Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMVR",
  "name": "AlphaVest Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATMVU",
  "name": "AlphaVest Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATNF",
  "name": "180 Life Sciences Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATNFW",
  "name": "180 Life Sciences Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATNI",
  "name": "ATN International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATOM",
  "name": "Atomera Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATOS",
  "name": "Atossa Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATPC",
  "name": "Agape ATP Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATRA",
  "name": "Atara Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATRC",
  "name": "AtriCure, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATRI",
  "name": "Atrion Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATRO",
  "name": "Astronics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATSG",
  "name": "Air Transport Services Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATXG",
  "name": "Addentax Group Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATXI",
  "name": "Avenue Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ATXS",
  "name": "Astria Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUBN",
  "name": "Auburn National Bancorporation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUDC",
  "name": "AudioCodes Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUGX",
  "name": "Augmedix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUID",
  "name": "authID Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUMI",
  "name": "Themes Gold Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUPH",
  "name": "Aurinia Pharmaceuticals Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUR",
  "name": "Aurora Innovation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AURA",
  "name": "Aura Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUROW",
  "name": "Aurora Innovation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUTL",
  "name": "Autolus Therapeutics plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUUD",
  "name": "Auddia Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUUDW",
  "name": "Auddia Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUVI",
  "name": "Applied UV, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AUVIP",
  "name": "Applied UV, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVAH",
  "name": "Aveanna Healthcare Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVAV",
  "name": "AeroVironment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVBP",
  "name": "ArriVent BioPharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVDL",
  "name": "Avadel Pharmaceuticals plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVDX",
  "name": "AvidXchange Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVGO",
  "name": "Broadcom Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVGR",
  "name": "Avinger, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVIR",
  "name": "Atea Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVNW",
  "name": "Aviat Networks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVO",
  "name": "Mission Produce, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVPT",
  "name": "AvePoint, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVPTW",
  "name": "AvePoint, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVRO",
  "name": "AVROBIO, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVT",
  "name": "Avnet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVTE",
  "name": "Aerovate Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVTX",
  "name": "Avalo Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVXC",
  "name": "Avantis Emerging Markets ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AVXL",
  "name": "Anavex Life Sciences Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AWH",
  "name": "Aspira Women's Health Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AWIN",
  "name": "AERWINS Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AWINW",
  "name": "AERWINS Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AWRE",
  "name": "Aware, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AXDX",
  "name": "Accelerate Diagnostics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AXGN",
  "name": "Axogen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AXNX",
  "name": "Axonics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AXON",
  "name": "Axon Enterprise, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AXSM",
  "name": "Axsome Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AXTI",
  "name": "AXT Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AY",
  "name": "Atlantica Sustainable Infrastructure plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AYRO",
  "name": "AYRO, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AYTU",
  "name": "Aytu BioPharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AZ",
  "name": "A2Z Smart Technologies Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AZN",
  "name": "AstraZeneca PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AZPN",
  "name": "Aspen Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "AZTA",
  "name": "Azenta, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BABX",
  "name": "GraniteShares 2x Long BABA Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BACK",
  "name": "IMAC Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAER",
  "name": "Bridger Aerospace Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAERW",
  "name": "Bridger Aerospace Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAFN",
  "name": "BayFirst Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAND",
  "name": "Bandwidth Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BANF",
  "name": "BancFirst Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BANFP",
  "name": "BancFirst Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BANL",
  "name": "CBL International Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BANR",
  "name": "Banner Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BANX",
  "name": "ArrowMark Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAOS",
  "name": "Baosheng Media Group Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BASE",
  "name": "Couchbase, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BATRA",
  "name": "Atlanta Braves Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BATRK",
  "name": "Atlanta Braves Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAYA",
  "name": "Bayview Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAYAR",
  "name": "Bayview Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BAYAU",
  "name": "Bayview Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBCP",
  "name": "Concrete Pumping Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBGI",
  "name": "Beasley Broadcast Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBH",
  "name": "VanEck Biotech ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBIO",
  "name": "BridgeBio Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBLG",
  "name": "Bone Biologics Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBLGW",
  "name": "Bone Biologics Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BBSI",
  "name": "Barrett Business Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCAB",
  "name": "BioAtla, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCAL",
  "name": "Southern California Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCAN",
  "name": "BYND Cannasoft Enterprises Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCBP",
  "name": "BCB Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCDA",
  "name": "BioCardia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCDAW",
  "name": "BioCardia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCG",
  "name": "Binah Capital Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCGWW",
  "name": "Binah Capital Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCLI",
  "name": "Brainstorm Cell Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCML",
  "name": "BayCom Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCOV",
  "name": "Brightcove Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCOW",
  "name": "1895 Bancorp of Wisconsin, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCPC",
  "name": "Balchem Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCRX",
  "name": "BioCryst Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCSA",
  "name": "Blockchain Coinvestors Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCSAU",
  "name": "Blockchain Coinvestors Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCSAW",
  "name": "Blockchain Coinvestors Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCTX",
  "name": "BriaCell Therapeutics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCTXW",
  "name": "BriaCell Therapeutics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BCYC",
  "name": "Bicycle Therapeutics plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BDGS",
  "name": "Bridges Capital Tactical ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BDRX",
  "name": "Biodexa Pharmaceuticals plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BDSX",
  "name": "Biodesix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BDTX",
  "name": "Black Diamond Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BEAM",
  "name": "Beam Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BEAT",
  "name": "Heartbeam, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BEATW",
  "name": "Heartbeam, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BECN",
  "name": "Beacon Roofing Supply, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BEEM",
  "name": "Beam Global ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BEEZ",
  "name": "Honeytree U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BELFA",
  "name": "Bel Fuse Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BELFB",
  "name": "Bel Fuse Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BENF",
  "name": "Beneficient ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BENFW",
  "name": "Beneficient ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BETR",
  "name": "Better Home & Finance Holding Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BETRW",
  "name": "Better Home & Finance Holding Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFC",
  "name": "Bank First Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFI",
  "name": "BurgerFi International Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFIIW",
  "name": "BurgerFi International Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFIN",
  "name": "BankFinancial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFRG",
  "name": "Bullfrog AI Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFRGW",
  "name": "Bullfrog AI Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFRI",
  "name": "Biofrontera Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFRIW",
  "name": "Biofrontera Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BFST",
  "name": "Business First Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BGC",
  "name": "BGC Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BGFV",
  "name": "Big 5 Sporting Goods Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BGLC",
  "name": "BioNexus Gene Lab Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BGNE",
  "name": "BeiGene, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BGRN",
  "name": "iShares USD Green Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BGXX",
  "name": "Bright Green Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHAC",
  "name": "Focus Impact BH3 Acquisition Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHACU",
  "name": "Focus Impact BH3 Acquisition Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHACW",
  "name": "Focus Impact BH3 Acquisition Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHAT",
  "name": "Blue Hat Interactive Entertainment Technology ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHF",
  "name": "Brighthouse Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHFAL",
  "name": "Brighthouse Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHFAM",
  "name": "Brighthouse Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHFAN",
  "name": "Brighthouse Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHFAO",
  "name": "Brighthouse Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHFAP",
  "name": "Brighthouse Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BHRB",
  "name": "Burke & Herbert Financial Services Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIAF",
  "name": "bioAffinity Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIAFW",
  "name": "bioAffinity Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIB",
  "name": "ProShares Ultra Nasdaq Biotechnology",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIDU",
  "name": "Baidu, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIGC",
  "name": "BigCommerce Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIIB",
  "name": "Biogen Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BILI",
  "name": "Bilibili Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIMI",
  "name": "BIMI International Medical Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIOL",
  "name": "Biolase, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIOR",
  "name": "Biora Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIOX",
  "name": "Bioceres Crop Solutions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIRD",
  "name": "Allbirds, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIS",
  "name": "ProShares UltraShort Nasdaq Biotechnology",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BITF",
  "name": "Bitfarms Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BITS",
  "name": "Global X Blockchain & Bitcoin Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BIVI",
  "name": "BioVie Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BJDX",
  "name": "Bluejay Diagnostics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BJK",
  "name": "VanEck Gaming ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BJRI",
  "name": "BJ's Restaurants, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKCH",
  "name": "Global X Blockchain ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKHAU",
  "name": "Black Hawk Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKIV",
  "name": "BNY Mellon Innovators ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKNG",
  "name": "Booking Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKR",
  "name": "Baker Hughes Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKWO",
  "name": "BNY Mellon Women's Opportunities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BKYI",
  "name": "BIO",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BL",
  "name": "BlackLine, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLAC",
  "name": "Bellevue Life Sciences Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLACR",
  "name": "Bellevue Life Sciences Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLACU",
  "name": "Bellevue Life Sciences Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLACW",
  "name": "Bellevue Life Sciences Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLBD",
  "name": "Blue Bird Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLBX",
  "name": "Blackboxstocks Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLCN",
  "name": "Siren Nasdaq NexGen Economy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLCR",
  "name": "BlackRock Large Cap Core ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLDE",
  "name": "Blade Air Mobility, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLDEW",
  "name": "Blade Air Mobility, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLDP",
  "name": "Ballard Power Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLEU",
  "name": "bleuacacia ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLEUR",
  "name": "bleuacacia ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLEUU",
  "name": "bleuacacia ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLEUW",
  "name": "bleuacacia ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLFS",
  "name": "BioLife Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLFY",
  "name": "Blue Foundry Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLIN",
  "name": "Bridgeline Digital, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLKB",
  "name": "Blackbaud, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLLD",
  "name": "JPMorgan Sustainable Infrastructure ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLMN",
  "name": "Bloomin' Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLNK",
  "name": "Blink Charging Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLRX",
  "name": "BioLineRx Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLTE",
  "name": "Belite Bio, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLUE",
  "name": "bluebird bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BLZE",
  "name": "Backblaze, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BMBL",
  "name": "Bumble Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BMEA",
  "name": "Biomea Fusion, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BMR",
  "name": "Beamr Imaging Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BMRA",
  "name": "Biomerica, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BMRC",
  "name": "Bank of Marin Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BMRN",
  "name": "BioMarin Pharmaceutical Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNAI",
  "name": "Brand Engagement Network Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNAIW",
  "name": "Brand Engagement Network Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BND",
  "name": "Vanguard Total Bond Market ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNDW",
  "name": "Vanguard Total World Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNDX",
  "name": "Vanguard Total International Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNGO",
  "name": "Bionano Genomics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNIX",
  "name": "Bannix Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNIXR",
  "name": "Bannix Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNIXW",
  "name": "Bannix Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNOX",
  "name": "Bionomics Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNR",
  "name": "Burning Rock Biotech Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNRG",
  "name": "Brenmiller Energy Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNTC",
  "name": "Benitec Biopharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNTX",
  "name": "BioNTech SE ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNZI",
  "name": "Banzai International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BNZIW",
  "name": "Banzai International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOCN",
  "name": "Blue Ocean Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOCNU",
  "name": "Blue Ocean Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOCNW",
  "name": "Blue Ocean Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOF",
  "name": "BranchOut Food Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOKF",
  "name": "BOK Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOLD",
  "name": "Boundless Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOLT",
  "name": "Bolt Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BON",
  "name": "Bon Natural Life Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOOM",
  "name": "DMC Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOSC",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOTJ",
  "name": "Bank of the James Financial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOTT",
  "name": "Themes Robotics & Automation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOTZ",
  "name": "Global X Robotics & Artificial Intelligence ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOWN",
  "name": "Bowen Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOWNR",
  "name": "Bowen Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOWNU",
  "name": "Bowen Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BOXL",
  "name": "Boxlight Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPMC",
  "name": "Blueprint Medicines Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPOP",
  "name": "Popular, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPOPM",
  "name": "Popular, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPRN",
  "name": "Princeton Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPTH",
  "name": "Bio",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPYPM",
  "name": "Brookfield Property Partners L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPYPN",
  "name": "Brookfield Property Partners L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPYPO",
  "name": "Brookfield Property Partners L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BPYPP",
  "name": "Brookfield Property Partners L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRAC",
  "name": "Broad Capital Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRACR",
  "name": "Broad Capital Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRACU",
  "name": "Broad Capital Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRAG",
  "name": "Bragg Gaming Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BREA",
  "name": "Brera Holdings PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BREZ",
  "name": "Breeze Holdings Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BREZR",
  "name": "Breeze Holdings Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BREZW",
  "name": "Breeze Holdings Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRFH",
  "name": "Barfresh Food Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRID",
  "name": "Bridgford Foods Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRKH",
  "name": "BurTech Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRKHU",
  "name": "BurTech Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRKHW",
  "name": "BurTech Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRKL",
  "name": "Brookline Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRKR",
  "name": "Bruker Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRLS",
  "name": "Borealis Foods Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRLSW",
  "name": "Borealis Foods Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRLT",
  "name": "Brilliant Earth Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRNS",
  "name": "Barinthus Biotherapeutics plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRNY",
  "name": "Burney U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BROG",
  "name": "Brooge Energy Limited  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BROGW",
  "name": "Brooge Energy Limited  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRP",
  "name": "The Baldwin Insurance Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRRR",
  "name": "Valkyrie Bitcoin Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRSH",
  "name": "Bruush Oral Care Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRSHW",
  "name": "Bruush Oral Care Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRTR",
  "name": "BlackRock Total Return ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRTX",
  "name": "BioRestorative Therapies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRY",
  "name": "Berry Corporation (bry) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BRZE",
  "name": "Braze, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSBK",
  "name": "Bogota Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCO",
  "name": "Invesco BulletShares 2024 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCP",
  "name": "Invesco BulletShares 2025 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCQ",
  "name": "Invesco BulletShares 2026 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCR",
  "name": "Invesco BulletShares 2027 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCS",
  "name": "Invesco BulletShares 2028 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCT",
  "name": "Invesco BulletShares 2029 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCU",
  "name": "Invesco BulletShares 2030 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCV",
  "name": "Invesco BulletShares 2031 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCW",
  "name": "Invesco BulletShares 2032 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSCX",
  "name": "Invesco BulletShares 2033 Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSET",
  "name": "Bassett Furniture Industries, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSFC",
  "name": "Blue Star Foods Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSGM",
  "name": "BioSig Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJO",
  "name": "Invesco BulletShares 2024 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJP",
  "name": "Invesco BulletShares 2025 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJQ",
  "name": "Invesco BulletShares 2026 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJR",
  "name": "Invesco BulletShares 2027 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJS",
  "name": "Invesco BulletShares 2028 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJT",
  "name": "Invesco BulletShares 2029 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJU",
  "name": "Invesco BulletShares 2030 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSJV",
  "name": "Invesco BulletShares 2031 High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMO",
  "name": "Invesco BulletShares 2024 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMP",
  "name": "Invesco BulletShares 2025 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMQ",
  "name": "Invesco BulletShares 2026 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMR",
  "name": "Invesco BulletShares 2027 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMS",
  "name": "Invesco BulletShares 2028 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMT",
  "name": "Invesco BulletShares 2029 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMU",
  "name": "Invesco BulletShares 2030 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMV",
  "name": "Invesco BulletShares 2031 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSMW",
  "name": "Invesco BulletShares 2032 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSRR",
  "name": "Sierra Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSSX",
  "name": "Invesco BulletShares 2033 Municipal Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSVN",
  "name": "Bank7 Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSVO",
  "name": "EA Bridgeway Omni Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BSY",
  "name": "Bentley Systems, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTAI",
  "name": "BioXcel Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTBD",
  "name": "BT Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTBDW",
  "name": "BT Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTBT",
  "name": "Bit Digital, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTCS",
  "name": "BTCS Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTCT",
  "name": "BTC Digital Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTCTW",
  "name": "BTC Digital Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTCY",
  "name": "Biotricity, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTDR",
  "name": "Bitdeer Technologies Group ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTEC",
  "name": "Principal Healthcare Innovators ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTF",
  "name": "Valkyrie Bitcoin and Ether Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTFX",
  "name": "Valkyrie Bitcoin Futures Leveraged Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTM",
  "name": "Bitcoin Depot Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTMD",
  "name": "Biote Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTMWW",
  "name": "Bitcoin Depot Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTOG",
  "name": "Bit Origin Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTSG",
  "name": "BrightSpring Health Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BTSGU",
  "name": "BrightSpring Health Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUFC",
  "name": "AB Conservative Buffer ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUG",
  "name": "Global X Cybersecurity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUJA",
  "name": "Bukit Jalil Global Acquisition 1 Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUJAR",
  "name": "Bukit Jalil Global Acquisition 1 Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUJAU",
  "name": "Bukit Jalil Global Acquisition 1 Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUJAW",
  "name": "Bukit Jalil Global Acquisition 1 Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BULD",
  "name": "Pacer BlueStar Engineering the Future ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BUSE",
  "name": "First Busey Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BVFL",
  "name": "BV Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BVS",
  "name": "Bioventus Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWAQ",
  "name": "Blue World Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWAQR",
  "name": "Blue World Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWAQU",
  "name": "Blue World Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWAQW",
  "name": "Blue World Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWAY",
  "name": "BrainsWay Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWB",
  "name": "Bridgewater Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWBBP",
  "name": "Bridgewater Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWEN",
  "name": "Broadwind, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWFG",
  "name": "Bankwell Financial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWMN",
  "name": "Bowman Consulting Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BWMX",
  "name": "Betterware de Mexico, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYFC",
  "name": "Broadway Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYND",
  "name": "Beyond Meat, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYNO",
  "name": "byNordic Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYNOU",
  "name": "byNordic Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYNOW",
  "name": "byNordic Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYRN",
  "name": "Byrna Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYSI",
  "name": "BeyondSpring, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BYU",
  "name": "BAIYU Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BZ",
  "name": "KANZHUN LIMITED ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BZFD",
  "name": "BuzzFeed, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BZFDW",
  "name": "BuzzFeed, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "BZUN",
  "name": "Baozun Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CA",
  "name": "Xtrackers California Municipal Bonds ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAAS",
  "name": "China Automotive Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CABA",
  "name": "Cabaletta Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAC",
  "name": "Camden National Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CACC",
  "name": "Credit Acceptance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CACG",
  "name": "ClearBridge All Cap Growth ESG ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CACO",
  "name": "Caravelle International Group ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CADL",
  "name": "Candel Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAFG",
  "name": "Pacer US Small Cap Cash Cows Growth Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAKE",
  "name": "The Cheesecake Factory Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CALB",
  "name": "California BanCorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CALC",
  "name": "CalciMedica, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CALM",
  "name": "Cal",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CALT",
  "name": "Calliditas Therapeutics AB ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CALY",
  "name": "BlackRock Short",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAMP",
  "name": "CalAmp Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAMT",
  "name": "Camtek Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAN",
  "name": "Canaan Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CANC",
  "name": "Tema Oncology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CANQ",
  "name": "Calamos Alternative Nasdaq & Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAPR",
  "name": "Capricor Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAPT",
  "name": "Captivision Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAPTW",
  "name": "Captivision Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAR",
  "name": "Avis Budget Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CARA",
  "name": "Cara Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CARE",
  "name": "Carter Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CARG",
  "name": "CarGurus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CARM",
  "name": "Carisma Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CART",
  "name": "Maplebear Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CARV",
  "name": "Carver Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CARZ",
  "name": "First Trust S",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CASH",
  "name": "Pathward Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CASI",
  "name": "CASI Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CASS",
  "name": "Cass Information Systems, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CASY",
  "name": "Caseys General Stores, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CATC",
  "name": "Cambridge Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CATH",
  "name": "Global X S&P 500 Catholic Values ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CATY",
  "name": "Cathay General Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CAUD",
  "name": "Collective Audience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBAN",
  "name": "Colony Bankcorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBAT",
  "name": "CBAK Energy Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBFV",
  "name": "CB Financial Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBNK",
  "name": "Capital Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBRG",
  "name": "Chain Bridge I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBRGU",
  "name": "Chain Bridge I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBRL",
  "name": "Cracker Barrel Old Country Store, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBSH",
  "name": "Commerce Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CBUS",
  "name": "Cibus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCAP",
  "name": "Crescent Capital BDC, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCB",
  "name": "Coastal Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCBG",
  "name": "Capital City Bank Group ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCCC",
  "name": "C4 Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCCS",
  "name": "CCC Intelligent Solutions Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCD",
  "name": "Calamos Dynamic Convertible & Income Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCEP",
  "name": "Coca",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCG",
  "name": "Cheche Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCGWW",
  "name": "Cheche Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCIXU",
  "name": "Churchill Capital Corp IX ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCLD",
  "name": "CareCloud, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCLDO",
  "name": "CareCloud, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCLDP",
  "name": "CareCloud, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCNE",
  "name": "CNB Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCNEP",
  "name": "CNB Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCOI",
  "name": "Cogent Communications Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCRN",
  "name": "Cross Country Healthcare, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCSB",
  "name": "Carbon Collective Short Duration Green Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCSI",
  "name": "Consensus Cloud Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCSO",
  "name": "Carbon Collective Climate Solutions U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCTG",
  "name": "CCSC Technology International Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCTS",
  "name": "Cactus Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCTSU",
  "name": "Cactus Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CCTSW",
  "name": "Cactus Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDAQ",
  "name": "Compass Digital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDAQU",
  "name": "Compass Digital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDAQW",
  "name": "Compass Digital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDC",
  "name": "VictoryShares US EQ Income Enhanced Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDIO",
  "name": "Cardio Diagnostics Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDIOW",
  "name": "Cardio Diagnostics Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDL",
  "name": "VictoryShares US Large Cap High Div Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDLX",
  "name": "Cardlytics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDMO",
  "name": "Avid Bioservices, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDNA",
  "name": "CareDx, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDNS",
  "name": "Cadence Design Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDRO",
  "name": "Codere Online Luxembourg, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDROW",
  "name": "Codere Online Luxembourg, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDT",
  "name": "Conduit Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDTG",
  "name": "CDT Environmental Technology Investment Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDTTW",
  "name": "Conduit Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDTX",
  "name": "Cidara Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDW",
  "name": "CDW Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDXC",
  "name": "ChromaDex Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDXS",
  "name": "Codexis, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDZI",
  "name": "Cadiz, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CDZIP",
  "name": "Cadiz, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CEAD",
  "name": "CEA Industries Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CEADW",
  "name": "CEA Industries Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CECO",
  "name": "CECO Environmental Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CEFA",
  "name": "Global X S&P Catholic Values Developed ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CEG",
  "name": "Constellation Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CELC",
  "name": "Celcuity Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CELH",
  "name": "Celsius Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CELU",
  "name": "Celularity Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CELUW",
  "name": "Celularity Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CELZ",
  "name": "Creative Medical Technology Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CENN",
  "name": "Cenntro Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CENT",
  "name": "Central Garden & Pet Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CENTA",
  "name": "Central Garden & Pet Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CENX",
  "name": "Century Aluminum Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CERE",
  "name": "Cerevel Therapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CERO",
  "name": "CERo Therapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CEROW",
  "name": "CERo Therapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CERS",
  "name": "Cerus Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CERT",
  "name": "Certara, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CETU",
  "name": "Cetus Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CETUR",
  "name": "Cetus Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CETUU",
  "name": "Cetus Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CETUW",
  "name": "Cetus Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CETX",
  "name": "Cemtrex Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CETY",
  "name": "Clean Energy Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CEVA",
  "name": "CEVA, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFA",
  "name": "VictoryShares US 500 Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFB",
  "name": "CrossFirst Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFBK",
  "name": "CF Bankshares Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFFI",
  "name": "C&F Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFFN",
  "name": "Capitol Federal Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFFS",
  "name": "CF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFFSU",
  "name": "CF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFFSW",
  "name": "CF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFLT",
  "name": "Confluent, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFO",
  "name": "VictoryShares US 500 Enhanced Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CFSB",
  "name": "CFSB Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CG",
  "name": "The Carlyle Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGABL",
  "name": "The Carlyle Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGBD",
  "name": "Carlyle Secured Lending, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGBDL",
  "name": "Carlyle Secured Lending, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGC",
  "name": "Canopy Growth Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGEM",
  "name": "Cullinan Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGEN",
  "name": "Compugen Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGNT",
  "name": "Cognyte Software Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGNX",
  "name": "Cognex Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGO",
  "name": "Calamos Global Total Return Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGON",
  "name": "CG Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CGTX",
  "name": "Cognition Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHCI",
  "name": "Comstock Holding Companies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHCO",
  "name": "City Holding Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHDN",
  "name": "Churchill Downs, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHEF",
  "name": "The Chefs' Warehouse, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHEK",
  "name": "Check",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHI",
  "name": "Calamos Convertible Opportunities and Income Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHK",
  "name": "Chesapeake Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHKEL",
  "name": "Chesapeake Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHKEW",
  "name": "Chesapeake Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHKEZ",
  "name": "Chesapeake Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHKP",
  "name": "Check Point Software Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHMG",
  "name": "Chemung Financial Corp  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHNR",
  "name": "China Natural Resources, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHPS",
  "name": "Xtrackers Semiconductor Select Equity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHR",
  "name": "Cheer Holding, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHRD",
  "name": "Chord Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHRS",
  "name": "Coherus BioSciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHRW",
  "name": "C.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHSCL",
  "name": "CHS Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHSCM",
  "name": "CHS Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHSCN",
  "name": "CHS Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHSCO",
  "name": "CHS Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHSCP",
  "name": "CHS Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHSN",
  "name": "Chanson International Holding ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHTR",
  "name": "Charter Communications, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHUY",
  "name": "Chuy's Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHW",
  "name": "Calamos Global Dynamic Income Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHX",
  "name": "ChampionX Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CHY",
  "name": "Calamos Convertible and High Income Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIBR",
  "name": "First Trust NASDAQ Cybersecurity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CID",
  "name": "VictoryShares International High Div Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIFR",
  "name": "Cipher Mining Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIFRW",
  "name": "Cipher Mining Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIGI",
  "name": "Colliers International Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIL",
  "name": "VictoryShares International Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CINF",
  "name": "Cincinnati Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CING",
  "name": "Cingulate Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CINGW",
  "name": "Cingulate Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CISO",
  "name": "CISO Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CISS",
  "name": "C3is Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CITE",
  "name": "Cartica Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CITEU",
  "name": "Cartica Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CITEW",
  "name": "Cartica Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIVB",
  "name": "Civista Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CIZ",
  "name": "VictoryShares Developed Enhanced Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CJET",
  "name": "Chijet Motor Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CJJD",
  "name": "China Jo",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CKPT",
  "name": "Checkpoint Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLAR",
  "name": "Clarus Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLBK",
  "name": "Columbia Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLBT",
  "name": "Cellebrite DI Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLBTW",
  "name": "Cellebrite DI Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLDX",
  "name": "Celldex Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLEU",
  "name": "China Liberal Education Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLFD",
  "name": "Clearfield, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLGN",
  "name": "CollPlant Biotechnologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLIR",
  "name": "ClearSign Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLLS",
  "name": "Cellectis S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLMB",
  "name": "Climb Global Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLMT",
  "name": "Calumet Specialty Products Partners, L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLNE",
  "name": "Clean Energy Fuels Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLNN",
  "name": "Clene Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLNNW",
  "name": "Clene Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOA",
  "name": "BlackRock AAA CLO ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOD",
  "name": "Themes Cloud Computing ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOE",
  "name": "Clover Leaf Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOER",
  "name": "Clover Leaf Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOEU",
  "name": "Clover Leaf Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOU",
  "name": "Global X Cloud Computing ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLOV",
  "name": "Clover Health Investments, Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLPS",
  "name": "CLPS Incorporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLPT",
  "name": "ClearPoint Neuro Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLRB",
  "name": "Cellectar Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLRC",
  "name": "ClimateRock ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLRCR",
  "name": "ClimateRock ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLRCU",
  "name": "ClimateRock ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLRCW",
  "name": "ClimateRock ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLRO",
  "name": "ClearOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLSD",
  "name": "Clearside Biomedical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLSK",
  "name": "CleanSpark, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLSM",
  "name": "Cabana Target Leading Sector Moderate ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLST",
  "name": "Catalyst Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLVR",
  "name": "Clever Leaves Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLVRW",
  "name": "Clever Leaves Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CLWT",
  "name": "Euro Tech Holdings Company Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMAX",
  "name": "CareMax, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMAXW",
  "name": "CareMax, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMBM",
  "name": "Cambium Networks Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMCA",
  "name": "Capitalworks Emerging Markets Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMCAU",
  "name": "Capitalworks Emerging Markets Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMCAW",
  "name": "Capitalworks Emerging Markets Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMCO",
  "name": "Columbus McKinnon Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMCSA",
  "name": "Comcast Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMCT",
  "name": "Creative Media & Community Trust Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CME",
  "name": "CME Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMLS",
  "name": "Cumulus Media Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMMB",
  "name": "Chemomab Therapeutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMND",
  "name": "Clearmind Medicine Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMPO",
  "name": "CompoSecure, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMPOW",
  "name": "CompoSecure, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMPR",
  "name": "Cimpress plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMPS",
  "name": "COMPASS Pathways Plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMPX",
  "name": "Compass Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMRX",
  "name": "Chimerix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CMTL",
  "name": "Comtech Telecommunications Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNCR",
  "name": "Range Cancer Therapeutics ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNDT",
  "name": "Conduent Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNET",
  "name": "ZW Data Action Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNEY",
  "name": "CN Energy Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNFR",
  "name": "Conifer Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNFRZ",
  "name": "Conifer Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNGL",
  "name": "Canna",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNGLU",
  "name": "Canna",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNGLW",
  "name": "Canna",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNOB",
  "name": "ConnectOne Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNOBP",
  "name": "ConnectOne Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNSL",
  "name": "Consolidated Communications Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNSP",
  "name": "CNS Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNTA",
  "name": "Centessa Pharmaceuticals plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNTB",
  "name": "Connect Biopharma Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNTG",
  "name": "Centogene N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNTX",
  "name": "Context Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNTY",
  "name": "Century Casinos, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNVS",
  "name": "Cineverse Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNXC",
  "name": "Concentrix Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CNXN",
  "name": "PC Connection, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COCH",
  "name": "Envoy Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COCHW",
  "name": "Envoy Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COCO",
  "name": "The Vita Coco Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COCP",
  "name": "Cocrystal Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CODA",
  "name": "Coda Octopus Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CODX",
  "name": "Co",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COEP",
  "name": "Coeptis Therapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COEPW",
  "name": "Coeptis Therapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COFS",
  "name": "ChoiceOne Financial Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COGT",
  "name": "Cogent Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COHU",
  "name": "Cohu, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COIN",
  "name": "Coinbase Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COKE",
  "name": "Coca",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COLB",
  "name": "Columbia Banking System, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COLL",
  "name": "Collegium Pharmaceutical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COLM",
  "name": "Columbia Sportswear Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COMM",
  "name": "CommScope Holding Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COMT",
  "name": "iShares GSCI Commodity Dynamic Roll Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CONL",
  "name": "GraniteShares 2x Long COIN Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CONN",
  "name": "Conn's, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COO",
  "name": "The Cooper Companies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COOL",
  "name": "Corner Growth Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COOLU",
  "name": "Corner Growth Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COOLW",
  "name": "Corner Growth Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COOP",
  "name": "Mr.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COOT",
  "name": "Australian Oilseeds Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COOTW",
  "name": "Australian Oilseeds Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COPJ",
  "name": "Sprott Junior Copper Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COPP",
  "name": "Sprott Copper Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CORT",
  "name": "Corcept Therapeutics Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CORZ",
  "name": "Core Scientific, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CORZW",
  "name": "Core Scientific, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CORZZ",
  "name": "Core Scientific, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COSM",
  "name": "Cosmos Health Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COST",
  "name": "Costco Wholesale Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COWG",
  "name": "Pacer US Large Cap Cash Cows Growth Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COWS",
  "name": "Amplify Cash Flow Dividend Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "COYA",
  "name": "Coya Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPBI",
  "name": "Central Plains Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPHC",
  "name": "Canterbury Park Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPIX",
  "name": "Cumberland Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPLP",
  "name": "Capital Product Partners L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPLS",
  "name": "AB Core Plus Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPOP",
  "name": "Pop Culture Group Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPRT",
  "name": "Copart, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPRX",
  "name": "Catalyst Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPSH",
  "name": "CPS Technologies Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPSS",
  "name": "Consumer Portfolio Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPTN",
  "name": "Cepton, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPTNW",
  "name": "Cepton, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CPZ",
  "name": "Calamos Long\/Short Equity & Dynamic Income Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRAI",
  "name": "CRA International,Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRBP",
  "name": "Corbus Pharmaceuticals Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRBU",
  "name": "Caribou Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRCT",
  "name": "Cricut, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRDF",
  "name": "Cardiff Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRDL",
  "name": "Cardiol Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRDO",
  "name": "Credo Technology Group Holding Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CREG",
  "name": "Smart Powerr Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRESW",
  "name": "Cresud S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRESY",
  "name": "Cresud S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CREV",
  "name": "Carbon Revolution Public Limited Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CREVW",
  "name": "Carbon Revolution Public Limited Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CREX",
  "name": "Creative Realities, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRGO",
  "name": "Freightos Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRGOW",
  "name": "Freightos Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRGX",
  "name": "CARGO Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRIS",
  "name": "Curis, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRKN",
  "name": "Crown Electrokinetics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRMD",
  "name": "CorMedix Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRML",
  "name": "Critical Metals Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRMLW",
  "name": "Critical Metals Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRMT",
  "name": "America's Car",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRNC",
  "name": "Cerence Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRNT",
  "name": "Ceragon Networks Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRNX",
  "name": "Crinetics Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRON",
  "name": "Cronos Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CROX",
  "name": "Crocs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRSP",
  "name": "CRISPR Therapeutics AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRSR",
  "name": "Corsair Gaming, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRTO",
  "name": "Criteo S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRUS",
  "name": "Cirrus Logic, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRVL",
  "name": "CorVel Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRVO",
  "name": "CervoMed Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRVS",
  "name": "Corvus Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRWD",
  "name": "CrowdStrike Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CRWS",
  "name": "Crown Crafts, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSA",
  "name": "VictoryShares US Small Cap Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSB",
  "name": "VictoryShares US Small Cap High Div Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSBR",
  "name": "Champions Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSCO",
  "name": "Cisco Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSF",
  "name": "VictoryShares US Discovery Enhanced Volatility Wtd ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSGP",
  "name": "CoStar Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSGS",
  "name": "CSG Systems International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSIQ",
  "name": "Canadian Solar Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSLM",
  "name": "CSLM Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSLMR",
  "name": "CSLM Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSLMU",
  "name": "CSLM Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSLMW",
  "name": "CSLM Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSLR",
  "name": "Complete Solaria, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSLRW",
  "name": "Complete Solaria, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSPI",
  "name": "CSP Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSQ",
  "name": "Calamos Strategic Total Return Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSSE",
  "name": "Chicken Soup for the Soul Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSSEL",
  "name": "Chicken Soup for the Soul Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSSEN",
  "name": "Chicken Soup for the Soul Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSSEP",
  "name": "Chicken Soup for the Soul Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSTE",
  "name": "Caesarstone Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSTL",
  "name": "Castle Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSWC",
  "name": "Capital Southwest Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSWCZ",
  "name": "Capital Southwest Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSWI",
  "name": "CSW Industrials, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CSX",
  "name": "CSX Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTAS",
  "name": "Cintas Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTBI",
  "name": "Community Trust Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTCX",
  "name": "Carmell Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTCXW",
  "name": "Carmell Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTEC",
  "name": "Global X CleanTech ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTHR",
  "name": "Charles & Colvard Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTKB",
  "name": "Cytek Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTLP",
  "name": "Cantaloupe, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTMX",
  "name": "CytomX Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTNM",
  "name": "Contineum Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTNT",
  "name": "Cheetah Net Supply Chain Service Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTRM",
  "name": "Castor Maritime Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTRN",
  "name": "Citi Trends, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTSH",
  "name": "Cognizant Technology Solutions Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTSO",
  "name": "Cytosorbents Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CTXR",
  "name": "Citius Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CUBA",
  "name": "The Herzfeld Caribbean Basin Fund, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CUE",
  "name": "Cue Biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CULL",
  "name": "Cullman Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CURI",
  "name": "CuriosityStream Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CURIW",
  "name": "CuriosityStream Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CUTR",
  "name": "Cutera, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVAC",
  "name": "CureVac N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVBF",
  "name": "CVB Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVCO",
  "name": "Cavco Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVGI",
  "name": "Commercial Vehicle Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVGW",
  "name": "Calavo Growers, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVII",
  "name": "Churchill Capital Corp VII ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVIIU",
  "name": "Churchill Capital Corp VII ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVIIW",
  "name": "Churchill Capital Corp VII ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVKD",
  "name": "Cadrenal Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVLG",
  "name": "Covenant Logistics Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVLT",
  "name": "Commvault Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVLY",
  "name": "Codorus Valley Bancorp, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVRX",
  "name": "CVRx, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CVV",
  "name": "CVD Equipment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CWBC",
  "name": "Community West Bancshares ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CWCO",
  "name": "Consolidated Water Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CWD",
  "name": "CaliberCos Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CWST",
  "name": "Casella Waste Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CXAI",
  "name": "CXApp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CXAIW",
  "name": "CXApp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CXDO",
  "name": "Crexendo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CXSE",
  "name": "WisdomTree China ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYBR",
  "name": "CyberArk Software Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYCC",
  "name": "Cyclacel Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYCCP",
  "name": "Cyclacel Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYCN",
  "name": "Cyclerion Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYN",
  "name": "Cyngn Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYRX",
  "name": "CryoPort, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYTH",
  "name": "Cyclo Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYTHW",
  "name": "Cyclo Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYTK",
  "name": "Cytokinetics, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CYTO",
  "name": "Altamira Therapeutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CZAR",
  "name": "Themes Natural Monopoly ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CZFS",
  "name": "Citizens Financial Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CZNC",
  "name": "Citizens & Northern Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CZR",
  "name": "Caesars Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "CZWI",
  "name": "Citizens Community Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DADA",
  "name": "Dada Nexus Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAIO",
  "name": "Data I\/O Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAKT",
  "name": "Daktronics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DALI",
  "name": "First Trust Dorsey Wright DALI 1 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DALN",
  "name": "DallasNews Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAPP",
  "name": "VanEck Digital Transformation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DARE",
  "name": "Dare Bioscience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DASH",
  "name": "DoorDash, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DATS",
  "name": "DatChat, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DATSW",
  "name": "DatChat, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAVE",
  "name": "Dave Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAVEW",
  "name": "Dave Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAWN",
  "name": "Day One Biopharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DAX",
  "name": "Global X DAX Germany ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DBGI",
  "name": "Digital Brands Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DBGIW",
  "name": "Digital Brands Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DBVT",
  "name": "DBV Technologies S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DBX",
  "name": "Dropbox, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DCBO",
  "name": "Docebo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DCGO",
  "name": "DocGo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DCOM",
  "name": "Dime Community Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DCOMP",
  "name": "Dime Community Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DCPH",
  "name": "Deciphera Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DCTH",
  "name": "Delcath Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DDI",
  "name": "DoubleDown Interactive Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DDIV",
  "name": "First Trust Dorsey Wright Momentum & Dividend ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DDOG",
  "name": "Datadog, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DECA",
  "name": "Denali Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DECAU",
  "name": "Denali Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DECAW",
  "name": "Denali Capital Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DEMZ",
  "name": "Democratic Large Cap Core ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DENN",
  "name": "Denny's Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DERM",
  "name": "Journey Medical Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DFGP",
  "name": "Dimensional Global Core Plus Fixed Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DFGX",
  "name": "Dimensional Global ex US Core Fixed Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DFLI",
  "name": "Dragonfly Energy Holdings Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DFLIW",
  "name": "Dragonfly Energy Holdings Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGCB",
  "name": "Dimensional Global Credit ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGHI",
  "name": "Digihost Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGICA",
  "name": "Donegal Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGICB",
  "name": "Donegal Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGII",
  "name": "Digi International Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGLY",
  "name": "Digital Ally, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGRE",
  "name": "WisdomTree Emerging Markets Quality Dividend Growth Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGRS",
  "name": "WisdomTree U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DGRW",
  "name": "WisdomTree U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DH",
  "name": "Definitive Healthcare Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHAC",
  "name": "Digital Health Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHACU",
  "name": "Digital Health Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHACW",
  "name": "Digital Health Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHAI",
  "name": "DIH Holding US, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHAIW",
  "name": "DIH Holding US, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHC",
  "name": "Diversified Healthcare Trust  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHCNI",
  "name": "Diversified Healthcare Trust  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHCNL",
  "name": "Diversified Healthcare Trust  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DHIL",
  "name": "Diamond Hill Investment Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DIBS",
  "name": "1stdibs.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DIOD",
  "name": "Diodes Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DIST",
  "name": "Distoken Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DISTR",
  "name": "Distoken Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DISTW",
  "name": "Distoken Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DIVD",
  "name": "Altrius Global Dividend ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DJCO",
  "name": "Daily Journal Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DJT",
  "name": "Trump Media & Technology Group Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DJTWW",
  "name": "Trump Media & Technology Group Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DKNG",
  "name": "DraftKings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DLHC",
  "name": "DLH Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DLO",
  "name": "DLocal Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DLPN",
  "name": "Dolphin Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DLTH",
  "name": "Duluth Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DLTR",
  "name": "Dollar Tree, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DMAC",
  "name": "DiaMedica Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DMAT",
  "name": "Global X Disruptive Materials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DMLP",
  "name": "Dorchester Minerals, L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DMRC",
  "name": "Digimarc Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DMTK",
  "name": "DermTech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DMXF",
  "name": "iShares ESG Advanced MSCI EAFE ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DNLI",
  "name": "Denali Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DNTH",
  "name": "Dianthus Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DNUT",
  "name": "Krispy Kreme, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOCU",
  "name": "DocuSign, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOGZ",
  "name": "Dogness (International) Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOMH",
  "name": "Dominari Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOMO",
  "name": "Domo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOOO",
  "name": "BRP Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DORM",
  "name": "Dorman Products, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOX",
  "name": "Amdocs Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DOYU",
  "name": "DouYu International Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DPCS",
  "name": "DP Cap Acquisition Corp I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DPCSU",
  "name": "DP Cap Acquisition Corp I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DPCSW",
  "name": "DP Cap Acquisition Corp I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DPRO",
  "name": "Draganfly Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRCT",
  "name": "Direct Digital Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRIO",
  "name": "DarioHealth Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRIV",
  "name": "Global X Autonomous & Electric Vehicles ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRMA",
  "name": "Dermata Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRMAW",
  "name": "Dermata Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRRX",
  "name": "DURECT Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRS",
  "name": "Leonardo DRS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRTS",
  "name": "Alpha Tau Medical Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRTSW",
  "name": "Alpha Tau Medical Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRUG",
  "name": "Bright Minds Biosciences Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DRVN",
  "name": "Driven Brands Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DSGN",
  "name": "Design Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DSGR",
  "name": "Distribution Solutions Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DSGX",
  "name": "The Descartes Systems Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DSP",
  "name": "Viant Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DSWL",
  "name": "Deswell Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTCK",
  "name": "Davis Commodities Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTCR",
  "name": "Global X Data Center & Digital Infrastructure ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTI",
  "name": "Drilling Tools International Corporation  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTIL",
  "name": "Precision BioSciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTSS",
  "name": "Datasea Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTST",
  "name": "Data Storage Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DTSTW",
  "name": "Data Storage Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DUET",
  "name": "DUET Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DUETU",
  "name": "DUET Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DUETW",
  "name": "DUET Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DUO",
  "name": "Fangdd Network Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DUOL",
  "name": "Duolingo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DUOT",
  "name": "Duos Technologies Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DVAL",
  "name": "BrandywineGLOBAL",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DVAX",
  "name": "Dynavax Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DVLU",
  "name": "First Trust Dorsey Wright Momentum & Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DVOL",
  "name": "First Trust Dorsey Wright Momentum & Low Volatility ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DVY",
  "name": "iShares Select Dividend ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DWAS",
  "name": "Invesco Dorsey Wright SmallCap Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DWAW",
  "name": "AdvisorShares Dorsey Wright FSM All Cap World ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DWSH",
  "name": "AdvisorShares Dorsey Wright Short ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DWSN",
  "name": "Dawson Geophysical Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DWUS",
  "name": "AdvisorShares Dorsey Wright FSM US Core ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DXCM",
  "name": "DexCom, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DXJS",
  "name": "WisdomTree Japan Hedged SmallCap Equity Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DXLG",
  "name": "Destination XL Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DXPE",
  "name": "DXP Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DXR",
  "name": "Daxor Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DXYN",
  "name": "The Dixie Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYAI",
  "name": "Dyadic International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYCQ",
  "name": "DT Cloud Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYCQR",
  "name": "DT Cloud Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYCQU",
  "name": "DT Cloud Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYFI",
  "name": "IDX Dynamic Fixed Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYN",
  "name": "Dyne Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYNI",
  "name": "IDX Dynamic Innovation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYNT",
  "name": "Dynatronics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DYTA",
  "name": "SGI Dynamic Tactical ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "DZSI",
  "name": "DZS Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EA",
  "name": "Electronic Arts Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EAST",
  "name": "Eastside Distilling, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EBAY",
  "name": "eBay Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EBC",
  "name": "Eastern Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EBIZ",
  "name": "Global X E",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EBMT",
  "name": "Eagle Bancorp Montana, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EBON",
  "name": "Ebang International Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EBTC",
  "name": "Enterprise Bancorp Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECBK",
  "name": "ECB Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECDA",
  "name": "ECD Automotive Design, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECDAW",
  "name": "ECD Automotive Design, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECOR",
  "name": "electroCore, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECOW",
  "name": "Pacer Emerging Markets Cash Cows 100 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECPG",
  "name": "Encore Capital Group Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECX",
  "name": "ECARX Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ECXWW",
  "name": "ECARX Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDAP",
  "name": "EDAP TMS S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDBL",
  "name": "Edible Garden AG Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDBLW",
  "name": "Edible Garden AG Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDIT",
  "name": "Editas Medicine, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDOC",
  "name": "Global X Telemedicine & Digital Health ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDRY",
  "name": "EuroDry Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDSA",
  "name": "Edesa Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDTK",
  "name": "Skillful Craftsman Education Technology Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EDUC",
  "name": "Educational Development Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EEFT",
  "name": "Euronet Worldwide, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EEIQ",
  "name": "EpicQuest Education Group International Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EEMA",
  "name": "iShares MSCI Emerging Markets Asia ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFAS",
  "name": "Global X MSCI SuperDividend EAFE ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFOI",
  "name": "Energy Focus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFRA",
  "name": "iShares Environmental Infrastructure and Industrials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFSC",
  "name": "Enterprise Financial Services Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFSCP",
  "name": "Enterprise Financial Services Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFTR",
  "name": "eFFECTOR Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EFTRW",
  "name": "eFFECTOR Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EGAN",
  "name": "eGain Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EGBN",
  "name": "Eagle Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EGHT",
  "name": "8x8 Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EGIO",
  "name": "Edgio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EGRX",
  "name": "Eagle Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EH",
  "name": "EHang Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EHLS",
  "name": "Even Herd Long Short ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EHTH",
  "name": "eHealth, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EJH",
  "name": "E",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EKG",
  "name": "First Trust Nasdaq Lux Digital Health Solutions ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EKSO",
  "name": "Ekso Bionics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELAB",
  "name": "Elevai Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELBM",
  "name": "Electra Battery Materials Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELDN",
  "name": "Eledon Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELEV",
  "name": "Elevation Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELSE",
  "name": "Electro",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELTK",
  "name": "Eltek Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELTX",
  "name": "Elicio Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELUT",
  "name": "Elutia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELVA",
  "name": "Electrovaya Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELVN",
  "name": "Enliven Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELWS",
  "name": "Earlyworks Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ELYM",
  "name": "Eliem Therapeutics, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EM",
  "name": "Smart Share Global Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMB",
  "name": "iShares J.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMBC",
  "name": "Embecta Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMCB",
  "name": "WisdomTree Emerging Markets Corporate Bond Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMCG",
  "name": "Embrace Change Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMCGR",
  "name": "Embrace Change Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMCGU",
  "name": "Embrace Change Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMCGW",
  "name": "Embrace Change Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMIF",
  "name": "iShares Emerging Markets Infrastructure ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMKR",
  "name": "EMCORE Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EML",
  "name": "Eastern Company (The) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMLD",
  "name": "FTAC Emerald Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMLDU",
  "name": "FTAC Emerald Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMLDW",
  "name": "FTAC Emerald Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMXC",
  "name": "iShares MSCI Emerging Markets ex China ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EMXF",
  "name": "iShares ESG Advanced MSCI EM ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENG",
  "name": "ENGlobal Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENGN",
  "name": "enGene Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENGNW",
  "name": "enGene Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENLT",
  "name": "Enlight Renewable Energy Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENLV",
  "name": "Enlivex Therapeutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENPH",
  "name": "Enphase Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENSC",
  "name": "Ensysce Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENSG",
  "name": "The Ensign Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENTA",
  "name": "Enanta Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENTG",
  "name": "Entegris, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENTR",
  "name": "ERShares Entrepreneurs ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENTX",
  "name": "Entera Bio Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENVB",
  "name": "Enveric Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENVX",
  "name": "Enovix Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ENZL",
  "name": "iShares MSCI New Zealand ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EOLS",
  "name": "Evolus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EOSE",
  "name": "Eos Energy Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EOSEW",
  "name": "Eos Energy Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EPIX",
  "name": "ESSA Pharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EPOW",
  "name": "Sunrise New Energy Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EPRX",
  "name": "Eupraxia Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EPSN",
  "name": "Epsilon Energy Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EQ",
  "name": "Equillium, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EQIX",
  "name": "Equinix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EQRR",
  "name": "ProShares Equities for Rising Rates ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERAS",
  "name": "Erasca, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERET",
  "name": "iShares Environmentally Aware Real Estate ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERIC",
  "name": "Ericsson ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERIE",
  "name": "Erie Indemnity Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERII",
  "name": "Energy Recovery, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERNA",
  "name": "Eterna Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ERNZ",
  "name": "TrueShares Active Yield ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESCA",
  "name": "Escalade, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESEA",
  "name": "Euroseas Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGD",
  "name": "iShares ESG Aware MSCI EAFE ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGE",
  "name": "iShares ESG Aware MSCI EM ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGL",
  "name": "ESGL Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGLW",
  "name": "ESGL Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGR",
  "name": "Enstar Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGRO",
  "name": "Enstar Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGRP",
  "name": "Enstar Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESGU",
  "name": "iShares ESG Aware MSCI USA ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESHA",
  "name": "ESH Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESHAR",
  "name": "ESH Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESLA",
  "name": "Estrella Immunopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESLAW",
  "name": "Estrella Immunopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESLT",
  "name": "Elbit Systems Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESMV",
  "name": "iShares ESG MSCI USA Min Vol Factor ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESOA",
  "name": "Energy Services of America Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESPO",
  "name": "VanEck Video Gaming and eSports ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESPR",
  "name": "Esperion Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESQ",
  "name": "Esquire Financial Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESSA",
  "name": "ESSA Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ESTA",
  "name": "Establishment Labs Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ETEC",
  "name": "iShares Breakthrough Environmental Solutions ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ETNB",
  "name": "89bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ETON",
  "name": "Eton Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ETSY",
  "name": "Etsy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EU",
  "name": "enCore Energy Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EUDA",
  "name": "Euda Health Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EUDAW",
  "name": "Euda Health Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EUFN",
  "name": "iShares MSCI Europe Financials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVAX",
  "name": "Evaxion Biotech A\/S ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVBG",
  "name": "Everbridge, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVCM",
  "name": "EverCommerce Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVER",
  "name": "EverQuote, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVGN",
  "name": "Evogene Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVGO",
  "name": "EVgo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVGOW",
  "name": "EVgo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVGR",
  "name": "Evergreen Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVGRU",
  "name": "Evergreen Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVGRW",
  "name": "Evergreen Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVLV",
  "name": "Evolv Technologies Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVLVW",
  "name": "Evolv Technologies Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVMT",
  "name": "Invesco Electric Vehicle Metals Commodity Strategy No K",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVO",
  "name": "Evotec SE ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVOK",
  "name": "Evoke Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVRG",
  "name": "Evergy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EVTV",
  "name": "Envirotech Vehicles, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EWBC",
  "name": "East West Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EWCZ",
  "name": "European Wax Center, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EWJV",
  "name": "iShares MSCI Japan Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EWTX",
  "name": "Edgewise Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EWZS",
  "name": "iShares MSCI Brazil Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXAI",
  "name": "Exscientia Plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXAS",
  "name": "Exact Sciences Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXC",
  "name": "Exelon Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXEL",
  "name": "Exelixis, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXFY",
  "name": "Expensify, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXLS",
  "name": "ExlService Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXPE",
  "name": "Expedia Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXPI",
  "name": "eXp World Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXPO",
  "name": "Exponent, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EXTR",
  "name": "Extreme Networks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EYE",
  "name": "National Vision Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EYEG",
  "name": "AB Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EYEN",
  "name": "Eyenovia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EYPT",
  "name": "EyePoint Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EZFL",
  "name": "EzFill Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EZGO",
  "name": "EZGO Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "EZPW",
  "name": "EZCORP, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FA",
  "name": "First Advantage Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAAR",
  "name": "First Trust Alternative Absolute Return Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAAS",
  "name": "DigiAsia Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAASW",
  "name": "DigiAsia Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAB",
  "name": "First Trust Multi Cap Value AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAD",
  "name": "First Trust Multi Cap Growth AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FALN",
  "name": "iShares Fallen Angels USD Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAMI",
  "name": "Farmmi, INC.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FANG",
  "name": "Diamondback Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FANH",
  "name": "Fanhua Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FARM",
  "name": "Farmer Brothers Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FARO",
  "name": "FARO Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAST",
  "name": "Fastenal Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FAT",
  "name": "FAT Brands Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FATBB",
  "name": "FAT Brands Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FATBP",
  "name": "FAT Brands Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FATBW",
  "name": "FAT Brands Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FATE",
  "name": "Fate Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBIO",
  "name": "Fortress Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBIOP",
  "name": "Fortress Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBIZ",
  "name": "First Business Financial Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBL",
  "name": "GraniteShares 2x Long META Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBLG",
  "name": "FibroBiologics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBMS",
  "name": "The First Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBNC",
  "name": "First Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBOT",
  "name": "Fidelity Disruptive Automation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBRX",
  "name": "Forte Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBYD",
  "name": "Falcon's Beyond Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBYDW",
  "name": "Falcon's Beyond Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FBZ",
  "name": "First Trust Brazil AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCA",
  "name": "First Trust China AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCAL",
  "name": "First Trust California Municipal High income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCAP",
  "name": "First Capital, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCBC",
  "name": "First Community Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCCO",
  "name": "First Community Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCEF",
  "name": "First Trust Income Opportunities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCEL",
  "name": "FuelCell Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCFS",
  "name": "FirstCash Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCNCA",
  "name": "First Citizens BancShares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCNCO",
  "name": "First Citizens BancShares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCNCP",
  "name": "First Citizens BancShares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCUV",
  "name": "Focus Universal Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FCVT",
  "name": "First Trust SSI Strategic Convertible Securities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDBC",
  "name": "Fidelity D & D Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDCF",
  "name": "Fidelity Disruptive Communications ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDFF",
  "name": "Fidelity Disruptive Finance ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDIF",
  "name": "Fidelity Disruptors ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDIG",
  "name": "Fidelity Crypto Industry and Digital Payments ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDIV",
  "name": "MarketDesk Focused U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDMT",
  "name": "4D Molecular Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDNI",
  "name": "First Trust Dow Jones International Internet ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDT",
  "name": "First Trust Developed Markets Ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDTS",
  "name": "First Trust Developed Markets ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDTX",
  "name": "Fidelity Disruptive Technology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FDUS",
  "name": "Fidus Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEAM",
  "name": "5E Advanced Materials, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEBO",
  "name": "Fenbo Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEIM",
  "name": "Frequency Electronics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FELE",
  "name": "Franklin Electric Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEM",
  "name": "First Trust Emerging Markets AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEMB",
  "name": "First Trust Emerging Markets Local Currency Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEMS",
  "name": "First Trust Emerging Markets Small Cap AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEMY",
  "name": "Femasys Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FENC",
  "name": "Fennec Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEP",
  "name": "First Trust Europe AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEPI",
  "name": "REX FANG & Innovation Equity Premium Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEUZ",
  "name": "First Trust Eurozone AlphaDEX ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEX",
  "name": "First Trust Large Cap Core AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEXD",
  "name": "Fintech Ecosystem Development Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEXDR",
  "name": "Fintech Ecosystem Development Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEXDU",
  "name": "Fintech Ecosystem Development Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FEXDW",
  "name": "Fintech Ecosystem Development Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFBC",
  "name": "First Financial Bancorp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFIC",
  "name": "Flushing Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFIE",
  "name": "Faraday Future Intelligent Electric Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFIEW",
  "name": "Faraday Future Intelligent Electric Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFIN",
  "name": "First Financial Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFIV",
  "name": "F5, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FFNW",
  "name": "First Financial Northwest, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGBI",
  "name": "First Guaranty Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGBIP",
  "name": "First Guaranty Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGEN",
  "name": "FibroGen, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGF",
  "name": "Fundamental Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGFPP",
  "name": "Fundamental Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGI",
  "name": "FGI Industries Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGIWW",
  "name": "FGI Industries Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FGM",
  "name": "First Trust Germany AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FHB",
  "name": "First Hawaiian, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FHLT",
  "name": "Future Health ESG Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FHLTU",
  "name": "Future Health ESG Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FHLTW",
  "name": "Future Health ESG Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FHTX",
  "name": "Foghorn Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIAC",
  "name": "Focus Impact Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIACU",
  "name": "Focus Impact Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIACW",
  "name": "Focus Impact Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIBK",
  "name": "First Interstate BancSystem, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FICS",
  "name": "First Trust International Developed Capital Strength ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FID",
  "name": "First Trust S&P International Dividend Aristocrats ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FINE",
  "name": "Themes European Luxury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FINW",
  "name": "FinWise Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FINX",
  "name": "Global X FinTech ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIP",
  "name": "FTAI Infrastructure Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FISI",
  "name": "Financial Institutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FITB",
  "name": "Fifth Third Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FITBI",
  "name": "Fifth Third Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FITBO",
  "name": "Fifth Third Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FITBP",
  "name": "Fifth Third Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIVE",
  "name": "Five Below, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIVN",
  "name": "Five9, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIXD",
  "name": "First Trust TCW Opportunistic Fixed Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIXT",
  "name": "Procure Disaster Recovery Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FIZZ",
  "name": "National Beverage Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FJP",
  "name": "First Trust Japan AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FKU",
  "name": "First Trust United Kingdom AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FKWL",
  "name": "Franklin Wireless Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLDB",
  "name": "Fidelity Low Duration Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLEX",
  "name": "Flex Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLFV",
  "name": "Feutune Light Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLFVR",
  "name": "Feutune Light Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLFVU",
  "name": "Feutune Light Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLFVW",
  "name": "Feutune Light Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLGC",
  "name": "Flora Growth Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLGT",
  "name": "Fulgent Genetics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLIC",
  "name": "The First of Long Island Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLJ",
  "name": "FLJ Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLL",
  "name": "Full House Resorts, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLN",
  "name": "First Trust Latin America AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLNC",
  "name": "Fluence Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLNT",
  "name": "Fluent, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLUX",
  "name": "Flux Power Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLWS",
  "name": "1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLXS",
  "name": "Flexsteel Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FLYW",
  "name": "Flywire Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMAO",
  "name": "Farmers & Merchants Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMB",
  "name": "First Trust Managed Municipal ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMBH",
  "name": "First Mid Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMED",
  "name": "Fidelity Disruptive Medicine ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMET",
  "name": "Fidelity Metaverse ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMHI",
  "name": "First Trust Municipal High Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMNB",
  "name": "Farmers National Banc Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMST",
  "name": "Foremost Lithium Resource & Technology Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FMSTW",
  "name": "Foremost Lithium Resource & Technology Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNCB",
  "name": "FNCB Bancorp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNCH",
  "name": "Finch Therapeutics Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNGR",
  "name": "FingerMotion, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNK",
  "name": "First Trust Mid Cap Value AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNKO",
  "name": "Funko, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNLC",
  "name": "First Bancorp, Inc (ME) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNVT",
  "name": "Finnovate Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNVTU",
  "name": "Finnovate Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNVTW",
  "name": "Finnovate Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNWB",
  "name": "First Northwest Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNWD",
  "name": "Finward Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNX",
  "name": "First Trust Mid Cap Core AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FNY",
  "name": "First Trust Mid Cap Growth AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FOLD",
  "name": "Amicus Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FONR",
  "name": "Fonar Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORA",
  "name": "Forian Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORD",
  "name": "Forward Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORL",
  "name": "Four Leaf Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORLU",
  "name": "Four Leaf Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORLW",
  "name": "Four Leaf Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORM",
  "name": "FormFactor, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORR",
  "name": "Forrester Research, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FORTY",
  "name": "Formula Systems (1985) Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FOSL",
  "name": "Fossil Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FOSLL",
  "name": "Fossil Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FOX",
  "name": "Fox Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FOXA",
  "name": "Fox Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FOXF",
  "name": "Fox Factory Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FPA",
  "name": "First Trust Asia Pacific Ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FPAY",
  "name": "FlexShopper, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FPXE",
  "name": "First Trust IPOX Europe Equity Opportunities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FPXI",
  "name": "First Trust International Equity Opportunities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRAF",
  "name": "Franklin Financial Services Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRBA",
  "name": "First Bank  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FREE",
  "name": "Whole Earth Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FREEW",
  "name": "Whole Earth Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRES",
  "name": "Fresh2 Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRGT",
  "name": "Freight Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRHC",
  "name": "Freedom Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRLA",
  "name": "Fortune Rise Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRLAU",
  "name": "Fortune Rise Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRLAW",
  "name": "Fortune Rise Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRME",
  "name": "First Merchants Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRMEP",
  "name": "First Merchants Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FROG",
  "name": "JFrog Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRPH",
  "name": "FRP Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRPT",
  "name": "Freshpet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRSH",
  "name": "Freshworks Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRST",
  "name": "Primis Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRSX",
  "name": "Foresight Autonomous Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FRZA",
  "name": "Forza X1, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSBC",
  "name": "Five Star Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSBW",
  "name": "FS Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSEA",
  "name": "First Seacoast Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSFG",
  "name": "First Savings Financial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSLR",
  "name": "First Solar, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSTR",
  "name": "L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSV",
  "name": "FirstService Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FSZ",
  "name": "First Trust Switzerland AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTA",
  "name": "First Trust Large Cap Value AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTAG",
  "name": "First Trust Indxx Global Agriculture ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTAI",
  "name": "FTAI Aviation Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTAIM",
  "name": "FTAI Aviation Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTAIN",
  "name": "FTAI Aviation Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTAIO",
  "name": "FTAI Aviation Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTAIP",
  "name": "FTAI Aviation Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTC",
  "name": "First Trust Large Cap Growth AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTCI",
  "name": "FTC Solar, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTCS",
  "name": "First Trust Capital Strength ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTDR",
  "name": "Frontdoor, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTDS",
  "name": "First Trust Dividend Strength ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTEK",
  "name": "Fuel Tech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTEL",
  "name": "Fitell Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTFT",
  "name": "Future FinTech Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTGC",
  "name": "First Trust Global Tactical Commodity Strategy Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTGS",
  "name": "First Trust Growth Strength ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTHI",
  "name": "First Trust BuyWrite Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTHM",
  "name": "Fathom Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTII",
  "name": "FutureTech II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTIIU",
  "name": "FutureTech II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTIIW",
  "name": "FutureTech II Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTLF",
  "name": "FitLife Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTNT",
  "name": "Fortinet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTQI",
  "name": "First Trust Nasdaq BuyWrite Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTRE",
  "name": "Fortrea Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTRI",
  "name": "First Trust Indxx Global Natural Resources Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTSL",
  "name": "First Trust Senior Loan Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTSM",
  "name": "First Trust Enhanced Short Maturity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTXG",
  "name": "First Trust Nasdaq Food & Beverage ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTXH",
  "name": "First Trust Nasdaq Pharmaceuticals ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTXL",
  "name": "First Trust Nasdaq Semiconductor ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTXN",
  "name": "First Trust Nasdaq Oil & Gas ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTXO",
  "name": "First Trust Nasdaq Bank ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FTXR",
  "name": "First Trust Nasdaq Transportation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUFU",
  "name": "BitFuFu Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUFUW",
  "name": "BitFuFu Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FULC",
  "name": "Fulcrum Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FULT",
  "name": "Fulton Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FULTP",
  "name": "Fulton Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUNC",
  "name": "First United Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUND",
  "name": "Sprott Focus Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUSB",
  "name": "First US Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUSN",
  "name": "Fusion Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FUTU",
  "name": "Futu Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FV",
  "name": "First Trust Dorsey Wright Focus 5 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FVC",
  "name": "First Trust Dorsey Wright Dynamic Focus 5 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FVCB",
  "name": "FVCBankcorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FWBI",
  "name": "First Wave BioPharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FWONA",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FWONK",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FWRD",
  "name": "Forward Air Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FWRG",
  "name": "First Watch Restaurant Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FXNC",
  "name": "First National Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FYBR",
  "name": "Frontier Communications Parent, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FYC",
  "name": "First Trust Small Cap Growth AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FYT",
  "name": "First Trust Small Cap Value AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "FYX",
  "name": "First Trust Small Cap Core AlphaDEX Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GABC",
  "name": "German American Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAIA",
  "name": "Gaia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAIN",
  "name": "Gladstone Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAINL",
  "name": "Gladstone Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAINN",
  "name": "Gladstone Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAINZ",
  "name": "Gladstone Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GALT",
  "name": "Galectin Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAMB",
  "name": "Gambling.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAMC",
  "name": "Golden Arrow Merger Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAMCU",
  "name": "Golden Arrow Merger Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAMCW",
  "name": "Golden Arrow Merger Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAME",
  "name": "GameSquare Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAN",
  "name": "GAN Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GANX",
  "name": "Gain Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GAQ",
  "name": "Generation Asia I Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GASS",
  "name": "StealthGas, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GATE",
  "name": "Marblegate Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GATEU",
  "name": "Marblegate Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GATEW",
  "name": "Marblegate Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GBBK",
  "name": "Global Blockchain Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GBBKR",
  "name": "Global Blockchain Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GBBKW",
  "name": "Global Blockchain Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GBDC",
  "name": "Golub Capital BDC, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GBIO",
  "name": "Generation Bio Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GBNY",
  "name": "Generations Bancorp NY, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GCBC",
  "name": "Greene County Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GCMG",
  "name": "GCM Grosvenor Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GCMGW",
  "name": "GCM Grosvenor Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GCT",
  "name": "GigaCloud Technology Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GCTK",
  "name": "GlucoTrack, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDC",
  "name": "GD Culture Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDEN",
  "name": "Golden Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDEV",
  "name": "GDEV Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDEVW",
  "name": "GDEV Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDHG",
  "name": "Golden Heaven Group Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDRX",
  "name": "GoodRx Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDS",
  "name": "GDS Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDST",
  "name": "Goldenstone Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDSTR",
  "name": "Goldenstone Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDSTU",
  "name": "Goldenstone Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDSTW",
  "name": "Goldenstone Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDTC",
  "name": "CytoMed Therapeutics Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GDYN",
  "name": "Grid Dynamics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GECC",
  "name": "Great Elm Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GECCI",
  "name": "Great Elm Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GECCM",
  "name": "Great Elm Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GECCO",
  "name": "Great Elm Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GECCZ",
  "name": "Great Elm Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GEG",
  "name": "Great Elm Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GEGGL",
  "name": "Great Elm Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GEHC",
  "name": "GE HealthCare Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GEN",
  "name": "Gen Digital Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GENE",
  "name": "Genetic Technologies Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GENK",
  "name": "GEN Restaurant Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GEOS",
  "name": "Geospace Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GERN",
  "name": "Geron Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GEVO",
  "name": "Gevo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GFAI",
  "name": "Guardforce AI Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GFAIW",
  "name": "Guardforce AI Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GFGF",
  "name": "Guru Favorite Stocks ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GFS",
  "name": "GlobalFoundries Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GGAL",
  "name": "Grupo Financiero Galicia S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GGLL",
  "name": "Direxion Daily GOOGL Bull 2X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GGLS",
  "name": "Direxion Daily GOOGL Bear 1X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GGR",
  "name": "Gogoro Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GGROW",
  "name": "Gogoro Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GH",
  "name": "Guardant Health, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GHIX",
  "name": "Gores Holdings IX, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GHIXU",
  "name": "Gores Holdings IX, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GHIXW",
  "name": "Gores Holdings IX, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GHRS",
  "name": "GH Research PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GHSI",
  "name": "Guardion Health Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GIFI",
  "name": "Gulf Island Fabrication, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GIGM",
  "name": "GigaMedia Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GIII",
  "name": "G",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GILD",
  "name": "Gilead Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GILT",
  "name": "Gilat Satellite Networks Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GINX",
  "name": "SGI Enhanced Global Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GIPR",
  "name": "Generation Income Properties Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GIPRW",
  "name": "Generation Income Properties Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLAC",
  "name": "Global Lights Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLACR",
  "name": "Global Lights Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLACU",
  "name": "Global Lights Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLAD",
  "name": "Gladstone Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLADZ",
  "name": "Gladstone Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLBE",
  "name": "Global",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLBS",
  "name": "Globus Maritime Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLBZ",
  "name": "Glen Burnie Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLDD",
  "name": "Great Lakes Dredge & Dock Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLDI",
  "name": "Credit Suisse X",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLLI",
  "name": "Globalink Investment Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLLIR",
  "name": "Globalink Investment Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLLIU",
  "name": "Globalink Investment Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLLIW",
  "name": "Globalink Investment Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLMD",
  "name": "Galmed Pharmaceuticals Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLNG",
  "name": "Golar LNG Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLPG",
  "name": "Galapagos NV ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLPI",
  "name": "Gaming and Leisure Properties, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLRE",
  "name": "Greenlight Reinsurance, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLSI",
  "name": "Greenwich LifeSciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLST",
  "name": "Global Star Acquisition, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLSTR",
  "name": "Global Star Acquisition, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLSTU",
  "name": "Global Star Acquisition, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLSTW",
  "name": "Global Star Acquisition, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLTO",
  "name": "Galecto, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLUE",
  "name": "Monte Rosa Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GLYC",
  "name": "GlycoMimetics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GMAB",
  "name": "Genmab A\/S ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GMFI",
  "name": "Aetherium Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GMFIU",
  "name": "Aetherium Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GMFIW",
  "name": "Aetherium Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GMGI",
  "name": "Golden Matrix Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GMM",
  "name": "Global Mofy Metaverse Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNFT",
  "name": "GENFIT S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNLN",
  "name": "Greenlane Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNLX",
  "name": "Genelux Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNMA",
  "name": "iShares GNMA Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNOM",
  "name": "Global X Genomics & Biotechnology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNPX",
  "name": "Genprex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNSS",
  "name": "Genasys Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNTA",
  "name": "Genenta Science S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GNTX",
  "name": "Gentex Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GO",
  "name": "Grocery Outlet Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOCO",
  "name": "GoHealth, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GODN",
  "name": "Golden Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GODNR",
  "name": "Golden Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GODNU",
  "name": "Golden Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOEV",
  "name": "Canoo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOEVW",
  "name": "Canoo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOGL",
  "name": "Golden Ocean Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOGO",
  "name": "Gogo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOOD",
  "name": "Gladstone Commercial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOODN",
  "name": "Gladstone Commercial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOODO",
  "name": "Gladstone Commercial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOOG",
  "name": "Alphabet Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOOGL",
  "name": "Alphabet Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GORV",
  "name": "Lazydays Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOSS",
  "name": "Gossamer Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOVI",
  "name": "Invesco Equal Weight 0",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOVX",
  "name": "GeoVax Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GOVXW",
  "name": "GeoVax Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GP",
  "name": "GreenPower Motor Company Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPAC",
  "name": "Global Partner Acquisition Corp II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPACU",
  "name": "Global Partner Acquisition Corp II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPACW",
  "name": "Global Partner Acquisition Corp II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPAK",
  "name": "Gamer Pakistan Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPCR",
  "name": "Structure Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPIQ",
  "name": "Goldman Sachs Nasdaq",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPIX",
  "name": "Goldman Sachs S&P 500 Core Premium Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPRE",
  "name": "Green Plains, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GPRO",
  "name": "GoPro, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRAB",
  "name": "Grab Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRABW",
  "name": "Grab Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRDI",
  "name": "GRIID Infrastructure Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRDIW",
  "name": "GRIID Infrastructure Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GREE",
  "name": "Greenidge Generation Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GREEL",
  "name": "Greenidge Generation Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRFS",
  "name": "Grifols, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRI",
  "name": "GRI Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRID",
  "name": "First Trust NASDAQ Clean Edge Smart Grid Infrastructure Index Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRIN",
  "name": "Grindrod Shipping Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRNQ",
  "name": "Greenpro Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GROM",
  "name": "Grom Social Enterprises Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GROMW",
  "name": "Grom Social Enterprises Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GROW",
  "name": "U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRPN",
  "name": "Groupon, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRRR",
  "name": "Gorilla Technology Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRRRW",
  "name": "Gorilla Technology Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRTS",
  "name": "Gritstone bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRTX",
  "name": "Galera Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRVY",
  "name": "GRAVITY Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRWG",
  "name": "GrowGeneration Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GRYP",
  "name": "Gryphon Digital Mining, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSBC",
  "name": "Great Southern Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSHD",
  "name": "Goosehead Insurance, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSIB",
  "name": "Themes Global Systemically Important Banks ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSIT",
  "name": "GSI Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSIW",
  "name": "Garden Stage Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSM",
  "name": "Ferroglobe PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSMGW",
  "name": "Cheer Holding, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GSUN",
  "name": "Golden Sun Health Technology Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GT",
  "name": "The Goodyear Tire & Rubber Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTAC",
  "name": "Global Technology Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTACU",
  "name": "Global Technology Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTACW",
  "name": "Global Technology Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTBP",
  "name": "GT Biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTEC",
  "name": "Greenland Technologies Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTHX",
  "name": "G1 Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTI",
  "name": "Graphjet Technology ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTIM",
  "name": "Good Times Restaurants Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTLB",
  "name": "GitLab Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTR",
  "name": "WisdomTree Target Range Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GTX",
  "name": "Garrett Motion Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GURE",
  "name": "Gulf Resources, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GUTS",
  "name": "Fractyl Health, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GV",
  "name": "Visionary Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GVH",
  "name": "Globavend Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GVP",
  "name": "GSE Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GWAV",
  "name": "Greenwave Technology Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GWRS",
  "name": "Global Water Resources, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GXAI",
  "name": "Gaxos.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GXTG",
  "name": "Global X Thematic Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GYRE",
  "name": "Gyre Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "GYRO",
  "name": "Gyrodyne , LLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HA",
  "name": "Hawaiian Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAFC",
  "name": "Hanmi Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAIA",
  "name": "Healthcare AI Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAIAU",
  "name": "Healthcare AI Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAIAW",
  "name": "Healthcare AI Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAIN",
  "name": "The Hain Celestial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HALO",
  "name": "Halozyme Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAO",
  "name": "Haoxi Health Technology Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAS",
  "name": "Hasbro, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HAYN",
  "name": "Haynes International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBAN",
  "name": "Huntington Bancshares Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBANL",
  "name": "Huntington Bancshares Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBANM",
  "name": "Huntington Bancshares Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBANP",
  "name": "Huntington Bancshares Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBCP",
  "name": "Home Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBIO",
  "name": "Harvard Bioscience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBNC",
  "name": "Horizon Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HBT",
  "name": "HBT Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCAT",
  "name": "Health Catalyst, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCKT",
  "name": "The Hackett Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCM",
  "name": "HUTCHMED (China) Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCOW",
  "name": "Amplify Cash Flow High Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCP",
  "name": "HashiCorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCSG",
  "name": "Healthcare Services Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCTI",
  "name": "Healthcare Triangle, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCVI",
  "name": "Hennessy Capital Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCVIU",
  "name": "Hennessy Capital Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCVIW",
  "name": "Hennessy Capital Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HCWB",
  "name": "HCW Biologics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HDSN",
  "name": "Hudson Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HEAR",
  "name": "Turtle Beach Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HEES",
  "name": "H&E Equipment Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HELE",
  "name": "Helen of Troy Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HEPA",
  "name": "Hepion Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HEPS",
  "name": "D",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HERD",
  "name": "Pacer Cash Cows Fund of Funds ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HERO",
  "name": "Global X Video Games & Esports ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HEWG",
  "name": "iShares Currency Hedged MSCI Germany ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HFBL",
  "name": "Home Federal Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HFFG",
  "name": "HF Foods Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HFWA",
  "name": "Heritage Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HGAS",
  "name": "Global Gas Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HGASW",
  "name": "Global Gas Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HGBL",
  "name": "Heritage Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HHGC",
  "name": "HHG Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HHGCR",
  "name": "HHG Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HHGCU",
  "name": "HHG Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HHGCW",
  "name": "HHG Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HHS",
  "name": "Harte Hanks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HIBB",
  "name": "Hibbett, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HIDE",
  "name": "Alpha Architect High Inflation and Deflation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HIFS",
  "name": "Hingham Institution for Savings ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HIHO",
  "name": "Highway Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HIMX",
  "name": "Himax Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HISF",
  "name": "First Trust High Income Strategic Focus ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HITI",
  "name": "High Tide Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HIVE",
  "name": "HIVE Digital Technologies Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HKIT",
  "name": "Hitek Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLAL",
  "name": "Wahed FTSE USA Shariah ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLIT",
  "name": "Harmonic Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLMN",
  "name": "Hillman Solutions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLNE",
  "name": "Hamilton Lane Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLP",
  "name": "Hongli Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLTH",
  "name": "Cue Health Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLVX",
  "name": "HilleVax, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HLXB",
  "name": "Helix Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HMNF",
  "name": "HMN Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HMST",
  "name": "HomeStreet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HNDL",
  "name": "Strategy Shares Nasdaq 7HANDL Index ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HNNA",
  "name": "Hennessy Advisors, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HNNAZ",
  "name": "Hennessy Advisors, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HNRG",
  "name": "Hallador Energy Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HNST",
  "name": "The Honest Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HNVR",
  "name": "Hanover Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOFT",
  "name": "Hooker Furnishings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOFV",
  "name": "Hall of Fame Resort & Entertainment Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOFVW",
  "name": "Hall of Fame Resort & Entertainment Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOLI",
  "name": "Hollysys Automation Technologies, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOLO",
  "name": "MicroCloud Hologram Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOLOW",
  "name": "MicroCloud Hologram Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOLX",
  "name": "Hologic, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HON",
  "name": "Honeywell International Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HONE",
  "name": "HarborOne Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOOD",
  "name": "Robinhood Markets, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOOK",
  "name": "HOOKIPA Pharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOPE",
  "name": "Hope Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOTH",
  "name": "Hoth Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOUR",
  "name": "Hour Loop, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOVNP",
  "name": "Hovnanian Enterprises Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOVR",
  "name": "New Horizon Aircraft Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOVRW",
  "name": "New Horizon Aircraft Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HOWL",
  "name": "Werewolf Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HPCO",
  "name": "Hempacco Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HPH",
  "name": "Highest Performances Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HPK",
  "name": "HighPeak Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HPKEW",
  "name": "HighPeak Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HQGO",
  "name": "Hartford US Quality Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HQI",
  "name": "HireQuest, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HQY",
  "name": "HealthEquity, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HRMY",
  "name": "Harmony Biosciences Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HROW",
  "name": "Harrow, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HROWL",
  "name": "Harrow, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HROWM",
  "name": "Harrow, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HRTS",
  "name": "Tema Obesity & Cardiometabolic ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HRTX",
  "name": "Heron Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HRYU",
  "name": "Hanryu Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HRZN",
  "name": "Horizon Technology Finance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSAI",
  "name": "Hesai Group ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSCS",
  "name": "Heart Test Laboratories, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSCSW",
  "name": "Heart Test Laboratories, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSDT",
  "name": "Helius Medical Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSIC",
  "name": "Henry Schein, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSII",
  "name": "Heidrick & Struggles International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSON",
  "name": "Hudson Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSPO",
  "name": "Horizon Space Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSPOR",
  "name": "Horizon Space Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSPOU",
  "name": "Horizon Space Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSPOW",
  "name": "Horizon Space Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HST",
  "name": "Host Hotels & Resorts, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HSTM",
  "name": "HealthStream, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTBI",
  "name": "HomeTrust Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTBK",
  "name": "Heritage Commerce Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTCR",
  "name": "Heartcore Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTHT",
  "name": "H World Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTIA",
  "name": "Healthcare Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTIBP",
  "name": "Healthcare Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTLD",
  "name": "Heartland Express, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTLF",
  "name": "Heartland Financial USA, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTLFP",
  "name": "Heartland Financial USA, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTOO",
  "name": "Fusion Fuel Green PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTOOW",
  "name": "Fusion Fuel Green PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTZ",
  "name": "Hertz Global Holdings, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HTZWW",
  "name": "Hertz Global Holdings, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUBC",
  "name": "Hub Cyber Security Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUBCW",
  "name": "Hub Cyber Security Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUBCZ",
  "name": "Hub Cyber Security Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUBG",
  "name": "Hub Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUDA",
  "name": "Hudson Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUDAR",
  "name": "Hudson Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUDAU",
  "name": "Hudson Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUDI",
  "name": "Huadi International Group Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUGE",
  "name": "FSD Pharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUIZ",
  "name": "Huize Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUMA",
  "name": "Humacyte, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUMAW",
  "name": "Humacyte, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HURC",
  "name": "Hurco Companies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HURN",
  "name": "Huron Consulting Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HUT",
  "name": "Hut 8 Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HWBK",
  "name": "Hawthorn Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HWC",
  "name": "Hancock Whitney Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HWCPZ",
  "name": "Hancock Whitney Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HWH",
  "name": "HWH International Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HWKN",
  "name": "Hawkins, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYDR",
  "name": "Global X Hydrogen ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYFM",
  "name": "Hydrofarm Holdings Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYLS",
  "name": "First Trust Tactical High Yield ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYMC",
  "name": "Hycroft Mining Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYMCL",
  "name": "Hycroft Mining Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYMCW",
  "name": "Hycroft Mining Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYPR",
  "name": "Hyperfine, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYW",
  "name": "Hywin Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYXF",
  "name": "iShares ESG Advanced High Yield Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYZD",
  "name": "WisdomTree Interest Rate Hedged High Yield Bond Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYZN",
  "name": "Hyzon Motors Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "HYZNW",
  "name": "Hyzon Motors Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IAC",
  "name": "IAC Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IART",
  "name": "Integra LifeSciences Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IAS",
  "name": "Integral Ad Science Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBAC",
  "name": "IB Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBACR",
  "name": "IB Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBAT",
  "name": "iShares Energy Storage & Materials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBB",
  "name": "iShares Biotechnology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBBQ",
  "name": "Invesco Nasdaq Biotechnology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBCP",
  "name": "Independent Bank Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBEX",
  "name": "IBEX Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBIT",
  "name": "iShares Bitcoin Trust",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBKR",
  "name": "Interactive Brokers Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBOC",
  "name": "International Bancshares Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBOT",
  "name": "VanEck Robotics ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBRX",
  "name": "ImmunityBio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTE",
  "name": "iShares iBonds Dec 2024 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTF",
  "name": "iShares iBonds Dec 2025 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTG",
  "name": "iShares iBonds Dec 2026 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTH",
  "name": "iShares iBonds Dec 2027 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTI",
  "name": "iShares iBonds Dec 2028 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTJ",
  "name": "iShares iBonds Dec 2029 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTK",
  "name": "iShares iBonds Dec 2030 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTL",
  "name": "iShares iBonds Dec 2031 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTM",
  "name": "iShares iBonds Dec 2032 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTO",
  "name": "iShares iBonds Dec 2033 Term Treasury ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IBTX",
  "name": "Independent Bank Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICAD",
  "name": "icad inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICCC",
  "name": "ImmuCell Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICCH",
  "name": "ICC Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICCM",
  "name": "IceCure Medical Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICCT",
  "name": "iCoreConnect Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICFI",
  "name": "ICF International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICG",
  "name": "Intchains Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICHR",
  "name": "Ichor Holdings ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICLK",
  "name": "iClick Interactive Asia Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICLN",
  "name": "iShares Global Clean Energy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICLR",
  "name": "ICON plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICMB",
  "name": "Investcorp Credit Management BDC, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICOP",
  "name": "iShares Copper and Metals Mining ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICU",
  "name": "SeaStar Medical Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICUCW",
  "name": "SeaStar Medical Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ICUI",
  "name": "ICU Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IDAI",
  "name": "T Stamp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IDCC",
  "name": "InterDigital, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IDEX",
  "name": "Ideanomics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IDN",
  "name": "Intellicheck, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IDXX",
  "name": "IDEXX Laboratories, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IDYA",
  "name": "IDEAYA Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IEF",
  "name": "iShares 7",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IEI",
  "name": "iShares 3",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IEP",
  "name": "Icahn Enterprises L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IESC",
  "name": "IES Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IEUS",
  "name": "iShares MSCI Europe Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IFBD",
  "name": "Infobird Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IFGL",
  "name": "iShares International Developed Real Estate ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IFRX",
  "name": "InflaRx N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IFV",
  "name": "First Trust Dorsey Wright International Focus 5 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGF",
  "name": "iShares Global Infrastructure ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGIB",
  "name": "iShares 5",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGIC",
  "name": "International General Insurance Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGMS",
  "name": "IGM Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGOV",
  "name": "iShares International Treasury Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGSB",
  "name": "iShares 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGTA",
  "name": "Inception Growth Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGTAR",
  "name": "Inception Growth Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGTAU",
  "name": "Inception Growth Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IGTAW",
  "name": "Inception Growth Acquisition Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IHRT",
  "name": "iHeartMedia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IHYF",
  "name": "Invesco High Yield Bond Factor ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "III",
  "name": "Information Services Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IIIV",
  "name": "i3 Verticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IINN",
  "name": "Inspira Technologies Oxy B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IINNW",
  "name": "Inspira Technologies Oxy B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IJT",
  "name": "iShares S&P SmallCap 600 Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IKNA",
  "name": "Ikena Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IKT",
  "name": "Inhibikase Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ILAG",
  "name": "Intelligent Living Application Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ILIT",
  "name": "iShares Lithium Miners and Producers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ILMN",
  "name": "Illumina, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ILPT",
  "name": "Industrial Logistics Properties Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMAB",
  "name": "I",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMAQ",
  "name": "International Media Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMAQR",
  "name": "International Media Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMAQU",
  "name": "International Media Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMAQW",
  "name": "International Media Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMCC",
  "name": "IM Cannabis Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMCR",
  "name": "Immunocore Holdings plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMCV",
  "name": "iShares Morningstar Mid",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMKTA",
  "name": "Ingles Markets, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMMP",
  "name": "Immutep Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMMR",
  "name": "Immersion Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMMX",
  "name": "Immix Biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMNM",
  "name": "Immunome, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMNN",
  "name": "Imunon, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMOM",
  "name": "Alpha Architect International Quantitative Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMOS",
  "name": "ChipMOS TECHNOLOGIES INC.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMPP",
  "name": "Imperial Petroleum Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMPPP",
  "name": "Imperial Petroleum Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMRN",
  "name": "Immuron Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMRX",
  "name": "Immuneering Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMTE",
  "name": "Integrated Media Technology Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMTX",
  "name": "Immatics N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMTXW",
  "name": "Immatics N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMUX",
  "name": "Immunic, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMVT",
  "name": "Immunovant, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IMXI",
  "name": "International Money Express, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INAB",
  "name": "IN8bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INAQ",
  "name": "Insight Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INAQU",
  "name": "Insight Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INAQW",
  "name": "Insight Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INBK",
  "name": "First Internet Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INBKZ",
  "name": "First Internet Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INBS",
  "name": "Intelligent Bio Solutions Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INBX",
  "name": "Inhibrx, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INCR",
  "name": "Intercure Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INCY",
  "name": "Incyte Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INDB",
  "name": "Independent Bank Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INDI",
  "name": "indie Semiconductor, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INDP",
  "name": "Indaptus Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INDV",
  "name": "Indivior PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INDY",
  "name": "iShares India 50 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INFN",
  "name": "Infinera Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INFR",
  "name": "ClearBridge Sustainable Infrastructure ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INGN",
  "name": "Inogen, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INHD",
  "name": "Inno Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INKT",
  "name": "MiNK Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INM",
  "name": "InMed Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INMB",
  "name": "INmune Bio Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INMD",
  "name": "InMode Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INNV",
  "name": "InnovAge Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INO",
  "name": "Inovio Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INOD",
  "name": "Innodata Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INRO",
  "name": "BlackRock U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INSE",
  "name": "Inspired Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INSG",
  "name": "Inseego Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INSM",
  "name": "Insmed Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTA",
  "name": "Intapp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTC",
  "name": "Intel Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTE",
  "name": "Integral Acquisition Corporation 1 ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTEU",
  "name": "Integral Acquisition Corporation 1 ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTEW",
  "name": "Integral Acquisition Corporation 1 ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTG",
  "name": "The Intergroup Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTJ",
  "name": "Intelligent Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTR",
  "name": "Inter & Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTS",
  "name": "Intensity Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTU",
  "name": "Intuit Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INTZ",
  "name": "Intrusion Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INVA",
  "name": "Innoviva, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INVE",
  "name": "Identiv, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INVO",
  "name": "INVO BioScience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INVZ",
  "name": "Innoviz Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INVZW",
  "name": "Innoviz Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "INZY",
  "name": "Inozyme Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IOBT",
  "name": "IO Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IONM",
  "name": "Assure Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IONR",
  "name": "ioneer Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IONS",
  "name": "Ionis Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IOSP",
  "name": "Innospec Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IOVA",
  "name": "Iovance Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPA",
  "name": "ImmunoPrecise Antibodies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPAR",
  "name": "Inter Parfums, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPDN",
  "name": "Professional Diversity Network, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPGP",
  "name": "IPG Photonics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPHA",
  "name": "Innate Pharma S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPKW",
  "name": "Invesco International BuyBack Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPSC",
  "name": "Century Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPW",
  "name": "iPower Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPWR",
  "name": "Ideal Power Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPX",
  "name": "IperionX Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPXX",
  "name": "Inflection Point Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPXXU",
  "name": "Inflection Point Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IPXXW",
  "name": "Inflection Point Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IQ",
  "name": "iQIYI, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IQQQ",
  "name": "ProShares Nasdaq",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRAA",
  "name": "Iris Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRAAU",
  "name": "Iris Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRAAW",
  "name": "Iris Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRBT",
  "name": "iRobot Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRDM",
  "name": "Iridium Communications Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IREN",
  "name": "Iris Energy Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRIX",
  "name": "IRIDEX Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRMD",
  "name": "iRadimed Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IROH",
  "name": "Iron Horse Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IROHR",
  "name": "Iron Horse Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IROHU",
  "name": "Iron Horse Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IROHW",
  "name": "Iron Horse Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRON",
  "name": "Disc Medicine, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IROQ",
  "name": "IF Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRTC",
  "name": "iRhythm Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IRWD",
  "name": "Ironwood Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISHG",
  "name": "iShares 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISHP",
  "name": "First Trust S",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISPC",
  "name": "iSpecimen Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISPO",
  "name": "Inspirato Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISPOW",
  "name": "Inspirato Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISPR",
  "name": "Ispire Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISRG",
  "name": "Intuitive Surgical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISRL",
  "name": "Israel Acquisitions Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISRLU",
  "name": "Israel Acquisitions Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISRLW",
  "name": "Israel Acquisitions Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISSC",
  "name": "Innovative Solutions and Support, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISTB",
  "name": "iShares Core 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISTR",
  "name": "Investar Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ISUN",
  "name": "iSun, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITCI",
  "name": "Intra",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITI",
  "name": "Iteris, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITIC",
  "name": "Investors Title Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITOS",
  "name": "iTeos Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITRI",
  "name": "Itron, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITRM",
  "name": "Iterum Therapeutics plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ITRN",
  "name": "Ituran Location and Control Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IUS",
  "name": "Invesco RAFI Strategic US ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IUSB",
  "name": "iShares Core Total USD Bond Market ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IUSG",
  "name": "iShares Core S&P U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IUSV",
  "name": "iShares Core S&P U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVA",
  "name": "Inventiva S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVAC",
  "name": "Intevac, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVAL",
  "name": "Alpha Architect International Quantitative Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCA",
  "name": "Investcorp India Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCAU",
  "name": "Investcorp India Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCAW",
  "name": "Investcorp India Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCB",
  "name": "Investcorp Europe Acquisition Corp I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCBU",
  "name": "Investcorp Europe Acquisition Corp I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCBW",
  "name": "Investcorp Europe Acquisition Corp I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCP",
  "name": "Swiftmerge Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCPU",
  "name": "Swiftmerge Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVCPW",
  "name": "Swiftmerge Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVDA",
  "name": "Iveda Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVDAW",
  "name": "Iveda Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVEG",
  "name": "iShares Emergent Food and AgTech Multisector ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVP",
  "name": "Inspire Veterinary Partners, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IVVD",
  "name": "Invivyd, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IWTR",
  "name": "iShares MSCI Water Management Multisector ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IXAQ",
  "name": "IX Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IXAQU",
  "name": "IX Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IXAQW",
  "name": "IX Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IXHL",
  "name": "Incannex Healthcare Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IXUS",
  "name": "iShares Core MSCI Total International Stock ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IZEA",
  "name": "IZEA Worldwide, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "IZM",
  "name": "ICZOOM Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JACK",
  "name": "Jack In The Box Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JAGX",
  "name": "Jaguar Health, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JAKK",
  "name": "JAKKS Pacific, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JAMF",
  "name": "Jamf Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JAN",
  "name": "JanOne Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JANX",
  "name": "Janux Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JAZZ",
  "name": "Jazz Pharmaceuticals plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JBHT",
  "name": "J.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JBLU",
  "name": "JetBlue Airways Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JBSS",
  "name": "John B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JCSE",
  "name": "JE Cleantech Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JCTCF",
  "name": "Jewett",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JD",
  "name": "JD.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JDOC",
  "name": "JPMorgan Healthcare Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JEPQ",
  "name": "JPMorgan Nasdaq Equity Premium Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JEWL",
  "name": "Adamas One Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JFBR",
  "name": "Jeffs' Brands Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JFBRW",
  "name": "Jeffs' Brands Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JFIN",
  "name": "Jiayin Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JFU",
  "name": "9F Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JG",
  "name": "Aurora Mobile Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JGLO",
  "name": "JPMorgan Global Select Equity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JIVE",
  "name": "JPMorgan International Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JJSF",
  "name": "J & J Snack Foods Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JKHY",
  "name": "Jack Henry & Associates, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JL",
  "name": "J",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JMSB",
  "name": "John Marshall Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JNVR",
  "name": "Janover Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JOUT",
  "name": "Johnson Outdoors Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JPEF",
  "name": "JPMorgan Equity Focus ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JRSH",
  "name": "Jerash Holdings (US), Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JRVR",
  "name": "James River Group Holdings, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JSM",
  "name": "Navient Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JSMD",
  "name": "Janus Henderson Small\/Mid Cap Growth Alpha ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JSML",
  "name": "Janus Henderson Small Cap Growth Alpha ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JSPR",
  "name": "Jasper Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JSPRW",
  "name": "Jasper Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JTAI",
  "name": "Jet.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JTAIW",
  "name": "Jet.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JTAIZ",
  "name": "Jet.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JTEK",
  "name": "JPMorgan U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JUNE",
  "name": "Junee Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JVA",
  "name": "Coffee Holding Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JVSA",
  "name": "JVSPAC Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JVSAR",
  "name": "JVSPAC Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JVSAU",
  "name": "JVSPAC Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JWEL",
  "name": "Jowell Global Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JXJT",
  "name": "JX Luxventure Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JYD",
  "name": "Jayud Global Logistics Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JYNT",
  "name": "The Joint Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JZ",
  "name": "Jianzhi Education Technology Group Company Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "JZXN",
  "name": "Jiuzi Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KA",
  "name": "Kineta, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KACL",
  "name": "Kairous Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KACLR",
  "name": "Kairous Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KACLU",
  "name": "Kairous Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KACLW",
  "name": "Kairous Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KALA",
  "name": "KALA BIO, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KALU",
  "name": "Kaiser Aluminum Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KALV",
  "name": "KalVista Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KARO",
  "name": "Karooooo Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KAVL",
  "name": "Kaival Brands Innovations Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KBWB",
  "name": "Invesco KBW Bank ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KBWD",
  "name": "Invesco KBW High Dividend Yield Financial ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KBWP",
  "name": "Invesco KBW Property & Casualty Insurance ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KBWR",
  "name": "Invesco KBW Regional Banking ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KBWY",
  "name": "Invesco KBW Premium Yield Equity REIT ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KC",
  "name": "Kingsoft Cloud Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KDP",
  "name": "Keurig Dr Pepper Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KE",
  "name": "Kimball Electronics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KEAT",
  "name": "Keating Active ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KELYA",
  "name": "Kelly Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KELYB",
  "name": "Kelly Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KEQU",
  "name": "Kewaunee Scientific Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KFFB",
  "name": "Kentucky First Federal Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KFRC",
  "name": "Kforce, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KGEI",
  "name": "Kolibri Global Energy Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KHC",
  "name": "The Kraft Heinz Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KIDS",
  "name": "OrthoPediatrics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KINS",
  "name": "Kingstone Companies, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KIRK",
  "name": "Kirkland's, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KITT",
  "name": "Nauticus Robotics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KITTW",
  "name": "Nauticus Robotics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KLAC",
  "name": "KLA Corporation  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KLIC",
  "name": "Kulicke and Soffa Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KLTR",
  "name": "Kaltura, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KLXE",
  "name": "KLX Energy Services Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KMDA",
  "name": "Kamada Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KNDI",
  "name": "Kandi Technologies Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KNGZ",
  "name": "First Trust S&P 500 Diversified Dividend Aristocrats ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KNSA",
  "name": "Kiniksa Pharmaceuticals, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KOD",
  "name": "Kodiak Sciences Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KOPN",
  "name": "Kopin Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KOSS",
  "name": "Koss Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KPLT",
  "name": "Katapult Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KPLTW",
  "name": "Katapult Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KPRX",
  "name": "Kiora Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KPTI",
  "name": "Karyopharm Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRKR",
  "name": "36Kr Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRMA",
  "name": "Global X Conscious Companies ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRMD",
  "name": "KORU Medical Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRNL",
  "name": "Kernel Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRNLU",
  "name": "Kernel Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRNLW",
  "name": "Kernel Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRNT",
  "name": "Kornit Digital Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRNY",
  "name": "Kearny Financial ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRON",
  "name": "Kronos Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KROP",
  "name": "Global X AgTech & Food Innovation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KROS",
  "name": "Keros Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRRO",
  "name": "Korro Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRT",
  "name": "Karat Packaging Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRUS",
  "name": "Kura Sushi USA, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KRYS",
  "name": "Krystal Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KSCP",
  "name": "Knightscope, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KSPI",
  "name": "Joint Stock Company Kaspi.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KTCC",
  "name": "Key Tronic Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KTOS",
  "name": "Kratos Defense & Security Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KTRA",
  "name": "Kintara Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KTTA",
  "name": "Pasithea Therapeutics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KTTAW",
  "name": "Pasithea Therapeutics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KURA",
  "name": "Kura Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KVAC",
  "name": "Keen Vision Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KVACU",
  "name": "Keen Vision Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KVACW",
  "name": "Keen Vision Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KVHI",
  "name": "KVH Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KWE",
  "name": "KWESST Micro Systems Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KWESW",
  "name": "KWESST Micro Systems Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KXIN",
  "name": "Kaixin Holdings ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KYMR",
  "name": "Kymera Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KYTX",
  "name": "Kyverna Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KZIA",
  "name": "Kazia Therapeutics Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "KZR",
  "name": "Kezar Life Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAB",
  "name": "Standard BioTools Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LABP",
  "name": "Landos Biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAES",
  "name": "SEALSQ Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAKE",
  "name": "Lakeland Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAMR",
  "name": "Lamar Advertising Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LANC",
  "name": "Lancaster Colony Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAND",
  "name": "Gladstone Land Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LANDM",
  "name": "Gladstone Land Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LANDO",
  "name": "Gladstone Land Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LANDP",
  "name": "Gladstone Land Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LARK",
  "name": "Landmark Bancorp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LASE",
  "name": "Laser Photonics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LASR",
  "name": "nLIGHT, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LATG",
  "name": "Chenghe Acquisition I Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LATGU",
  "name": "Chenghe Acquisition I Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAUR",
  "name": "Laureate Education, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LAZR",
  "name": "Luminar Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBAI",
  "name": "Lakeland Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBPH",
  "name": "Longboard Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBRDA",
  "name": "Liberty Broadband Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBRDK",
  "name": "Liberty Broadband Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBRDP",
  "name": "Liberty Broadband Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBTYA",
  "name": "Liberty Global Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBTYB",
  "name": "Liberty Global Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LBTYK",
  "name": "Liberty Global Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LCFY",
  "name": "Locafy Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LCFYW",
  "name": "Locafy Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LCID",
  "name": "Lucid Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LCNB",
  "name": "LCNB Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LCUT",
  "name": "Lifetime Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LDEM",
  "name": "iShares ESG MSCI EM Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LDSF",
  "name": "First Trust Low Duration Strategic Focus ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LDTC",
  "name": "LeddarTech Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LDTCW",
  "name": "LeddarTech Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LDWY",
  "name": "Lendway, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LE",
  "name": "Lands' End, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LECO",
  "name": "Lincoln Electric Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEDS",
  "name": "SemiLEDS Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEE",
  "name": "Lee Enterprises, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEGH",
  "name": "Legacy Housing Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEGN",
  "name": "Legend Biotech Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEGR",
  "name": "First Trust Indxx Innovative Transaction & Process ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LENZ",
  "name": "LENZ Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LESL",
  "name": "Leslie's, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEXX",
  "name": "Lexaria Bioscience Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LEXXW",
  "name": "Lexaria Bioscience Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFCR",
  "name": "Lifecore Biomedical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFLY",
  "name": "Leafly Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFLYW",
  "name": "Leafly Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFMD",
  "name": "LifeMD, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFMDP",
  "name": "LifeMD, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFST",
  "name": "LifeStance Health Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFUS",
  "name": "Littelfuse, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFVN",
  "name": "Lifevantage Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LFWD",
  "name": "ReWalk Robotics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGCB",
  "name": "Linkage Global Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGCL",
  "name": "Lucas GC Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGHL",
  "name": "Lion Group Holding Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGHLW",
  "name": "Lion Group Holding Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGIH",
  "name": "LGI Homes, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGMK",
  "name": "LogicMark, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGND",
  "name": "Ligand Pharmaceuticals Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGO",
  "name": "Largo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGRO",
  "name": "Level Four Large Cap Growth Active ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LGVN",
  "name": "Longeveron Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LI",
  "name": "Li Auto Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LICN",
  "name": "Lichen China Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIDR",
  "name": "AEye, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIDRW",
  "name": "AEye, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIFE",
  "name": "aTyr Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIFW",
  "name": "MSP Recovery, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIFWW",
  "name": "MSP Recovery, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIFWZ",
  "name": "MSP Recovery, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LILA",
  "name": "Liberty Latin America Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LILAK",
  "name": "Liberty Latin America Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LILM",
  "name": "Lilium N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LILMW",
  "name": "Lilium N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIN",
  "name": "Linde plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LINC",
  "name": "Lincoln Educational Services Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIND",
  "name": "Lindblad Expeditions Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LINK",
  "name": "Interlink Electronics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIPO",
  "name": "Lipella Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIQT",
  "name": "LiqTech International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LITE",
  "name": "Lumentum Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LITM",
  "name": "Snow Lake Resources Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LITP",
  "name": "Sprott Lithium Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIVE",
  "name": "Live Ventures Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIVN",
  "name": "LivaNova PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIXT",
  "name": "Lixte Biotechnology Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LIXTW",
  "name": "Lixte Biotechnology Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LKCO",
  "name": "Luokung Technology Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LKFN",
  "name": "Lakeland Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LKQ",
  "name": "LKQ Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LLYVA",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LLYVK",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LMAT",
  "name": "LeMaitre Vascular, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LMB",
  "name": "Limbach Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LMBS",
  "name": "First Trust Low Duration Opportunities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LMFA",
  "name": "LM Funding America, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LMNR",
  "name": "Limoneira Co ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNKB",
  "name": "LINKBANCORP, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNSR",
  "name": "LENSAR, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNT",
  "name": "Alliant Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNTH",
  "name": "Lantheus Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNW",
  "name": "Light & Wonder, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNZA",
  "name": "LanzaTech Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LNZAW",
  "name": "LanzaTech Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOAN",
  "name": "Manhattan Bridge Capital, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOBO",
  "name": "LOBO EV TECHNOLOGIES LTD.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOCO",
  "name": "El Pollo Loco Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOGI",
  "name": "Logitech International S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOOP",
  "name": "Loop Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOPE",
  "name": "Grand Canyon Education, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOT",
  "name": "Lotus Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOTWW",
  "name": "Lotus Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LOVE",
  "name": "The Lovesac Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LPCN",
  "name": "Lipocine Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LPLA",
  "name": "LPL Financial Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LPRO",
  "name": "Open Lending Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LPSN",
  "name": "LivePerson, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LPTH",
  "name": "LightPath Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LPTX",
  "name": "Leap Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LQDA",
  "name": "Liquidia Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LQDT",
  "name": "Liquidity Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LQR",
  "name": "LQR House Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRCX",
  "name": "Lam Research Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRE",
  "name": "Lead Real Estate Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRFC",
  "name": "Logan Ridge Finance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRGE",
  "name": "ClearBridge Large Cap Growth ESG ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRHC",
  "name": "La Rosa Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRMR",
  "name": "Larimar Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LRND",
  "name": "IQ U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSAK",
  "name": "Lesaka Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSBK",
  "name": "Lake Shore Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSCC",
  "name": "Lattice Semiconductor Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSDI",
  "name": "Lucy Scientific Discovery Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSEA",
  "name": "Landsea Homes Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSEAW",
  "name": "Landsea Homes Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSTA",
  "name": "Lisata Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSTR",
  "name": "Landstar System, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSXMA",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSXMB",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LSXMK",
  "name": "Liberty Media Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LTBR",
  "name": "Lightbridge Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LTRN",
  "name": "Lantern Pharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LTRX",
  "name": "Lantronix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LTRY",
  "name": "Lottery.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LTRYW",
  "name": "Lottery.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUCD",
  "name": "Lucid Diagnostics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUCY",
  "name": "Innovative Eyewear, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUCYW",
  "name": "Innovative Eyewear, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LULU",
  "name": "lululemon athletica inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUMO",
  "name": "Lumos Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUNA",
  "name": "Luna Innovations Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUNG",
  "name": "Pulmonx Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUNR",
  "name": "Intuitive Machines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUNRW",
  "name": "Intuitive Machines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUXH",
  "name": "LuxUrban Hotels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LUXHP",
  "name": "LuxUrban Hotels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LVHD",
  "name": "Franklin U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LVLU",
  "name": "Lulu's Fashion Lounge Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LVO",
  "name": "LiveOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LVRO",
  "name": "Lavoro Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LVROW",
  "name": "Lavoro Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LVTX",
  "name": "LAVA Therapeutics N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LWAY",
  "name": "Lifeway Foods, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LWLG",
  "name": "Lightwave Logic, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LX",
  "name": "LexinFintech Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LXEH",
  "name": "Lixiang Education Holding Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LXEO",
  "name": "Lexeo Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LXRX",
  "name": "Lexicon Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LYEL",
  "name": "Lyell Immunopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LYFT",
  "name": "Lyft, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LYRA",
  "name": "Lyra Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LYT",
  "name": "Lytus Technologies Holdings PTV.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LYTS",
  "name": "LSI Industries Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "LZ",
  "name": "LegalZoom.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MACA",
  "name": "Moringa Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MACAU",
  "name": "Moringa Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MACAW",
  "name": "Moringa Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MACK",
  "name": "Merrimack Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAGQ",
  "name": "Roundhill Daily Inverse Magnificent Seven ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAGS",
  "name": "Roundhill Magnificent Seven ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAGX",
  "name": "Roundhill Daily 2X Long Magnificent Seven ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAMA",
  "name": "Mama's Creations, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAMO",
  "name": "Massimo Group ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MANH",
  "name": "Manhattan Associates, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAPS",
  "name": "WM Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAPSW",
  "name": "WM Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAQC",
  "name": "Maquia Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAQCU",
  "name": "Maquia Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAQCW",
  "name": "Maquia Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAR",
  "name": "Marriott International ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MARA",
  "name": "Marathon Digital Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MARPS",
  "name": "Marine Petroleum Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MARX",
  "name": "Mars Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MARXR",
  "name": "Mars Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MARXU",
  "name": "Mars Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MASI",
  "name": "Masimo Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MASS",
  "name": "908 Devices Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAT",
  "name": "Mattel, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MATH",
  "name": "Metalpha Technology Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MATW",
  "name": "Matthews International Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAXI",
  "name": "Simplify Bitcoin Strategy PLUS Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAXN",
  "name": "Maxeon Solar Technologies, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MAYS",
  "name": "J.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBB",
  "name": "iShares MBS ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBCN",
  "name": "Middlefield Banc Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBIN",
  "name": "Merchants Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBINM",
  "name": "Merchants Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBINN",
  "name": "Merchants Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBINO",
  "name": "Merchants Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBIO",
  "name": "Mustang Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBLY",
  "name": "Mobileye Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBNKP",
  "name": "Medallion Bank ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBOT",
  "name": "Microbot Medical Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBRX",
  "name": "Moleculin Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBUU",
  "name": "Malibu Boats, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MBWM",
  "name": "Mercantile Bank Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAA",
  "name": "Mountain  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAAU",
  "name": "Mountain  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAAW",
  "name": "Mountain  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAC",
  "name": "Monterey Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCACR",
  "name": "Monterey Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCACU",
  "name": "Monterey Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCACW",
  "name": "Monterey Capital Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAG",
  "name": "Mountain Crest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAGR",
  "name": "Mountain Crest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCAGU",
  "name": "Mountain Crest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCBC",
  "name": "Macatawa Bank Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCBS",
  "name": "MetroCity Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCFT",
  "name": "MasterCraft Boat Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCHI",
  "name": "iShares MSCI China ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCHP",
  "name": "Microchip Technology Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCHS",
  "name": "Matthews China Discovery Active ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCHX",
  "name": "Marchex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCRB",
  "name": "Seres Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCRI",
  "name": "Monarch Casino & Resort, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCSE",
  "name": "Martin Currie Sustainable International Equity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MCVT",
  "name": "Mill City Ventures III, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDAI",
  "name": "Spectral AI, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDAIW",
  "name": "Spectral AI, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDB",
  "name": "MongoDB, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDBH",
  "name": "MDB Capital Holdings, LLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDCP",
  "name": "VictoryShares THB Mid Cap ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDGL",
  "name": "Madrigal Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDIA",
  "name": "Mediaco Holding Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDIV",
  "name": "Multi",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDJH",
  "name": "MDJM LTD ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDLZ",
  "name": "Mondelez International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDRR",
  "name": "Medalist Diversified REIT, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDRRP",
  "name": "Medalist Diversified REIT, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDWD",
  "name": "MediWound Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDXG",
  "name": "MiMedx Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MDXH",
  "name": "MDxHealth SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ME",
  "name": "23andMe Holding Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEDP",
  "name": "Medpace Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEDS",
  "name": "TRxADE HEALTH, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEDX",
  "name": "Horizon Kinetics Medical ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEGL",
  "name": "Magic Empire Global Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEIP",
  "name": "MEI Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MELI",
  "name": "MercadoLibre, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEMS",
  "name": "Matthews Emerging Markets Discovery Active ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MEOH",
  "name": "Methanex Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MERC",
  "name": "Mercer International Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MESA",
  "name": "Mesa Air Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MESO",
  "name": "Mesoblast Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "META",
  "name": "Meta Platforms, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "METC",
  "name": "Ramaco Resources, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "METCB",
  "name": "Ramaco Resources, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "METCL",
  "name": "Ramaco Resources, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MFH",
  "name": "Mercurity Fintech Holding Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MFI",
  "name": "mF International Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MFIC",
  "name": "MidCap Financial Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MFICL",
  "name": "MidCap Financial Investment Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MFIN",
  "name": "Medallion Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MFLX",
  "name": "First Trust Flexible Municipal High Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGEE",
  "name": "MGE Energy Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGIC",
  "name": "Magic Software Enterprises Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGIH",
  "name": "Millennium Group International Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGNI",
  "name": "Magnite, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGNX",
  "name": "MacroGenics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGOL",
  "name": "MGO Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGPI",
  "name": "MGP Ingredients, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGRC",
  "name": "McGrath RentCorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGRM",
  "name": "Monogram Orthopaedics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGRX",
  "name": "Mangoceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGTX",
  "name": "MeiraGTx Holdings plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGX",
  "name": "Metagenomi, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MGYR",
  "name": "Magyar Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MHLD",
  "name": "Maiden Holdings, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MHUA",
  "name": "Meihua International Medical Technologies Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MICS",
  "name": "The Singing Machine Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MIDD",
  "name": "The Middleby Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MIGI",
  "name": "Mawson Infrastructure Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MILN",
  "name": "Global X Millennial Consumer ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MIND",
  "name": "MIND Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MINDP",
  "name": "MIND Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MINM",
  "name": "Minim, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MIRA",
  "name": "MIRA Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MIRM",
  "name": "Mirum Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MIST",
  "name": "Milestone Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MITA",
  "name": "Coliseum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MITAU",
  "name": "Coliseum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MITAW",
  "name": "Coliseum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MITK",
  "name": "Mitek Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MKAM",
  "name": "MKAM ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MKSI",
  "name": "MKS Instruments, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MKTW",
  "name": "MarketWise, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MKTX",
  "name": "MarketAxess Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLAB",
  "name": "Mesa Laboratories, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLCO",
  "name": "Melco Resorts & Entertainment Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLEC",
  "name": "Moolec Science SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLECW",
  "name": "Moolec Science SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLGO",
  "name": "MicroAlgo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLKN",
  "name": "MillerKnoll, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLTX",
  "name": "MoonLake Immunotherapeutics ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MLYS",
  "name": "Mineralys Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MMAT",
  "name": "Meta Materials Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MMLP",
  "name": "Martin Midstream Partners L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MMSI",
  "name": "Merit Medical Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MMV",
  "name": "MultiMetaVerse Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MMVWW",
  "name": "MultiMetaVerse Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MMYT",
  "name": "MakeMyTrip Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNDO",
  "name": "MIND C.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNDR",
  "name": "Mobile",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNDY",
  "name": "monday.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNKD",
  "name": "MannKind Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNMD",
  "name": "Mind Medicine (MindMed) Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNOV",
  "name": "MediciNova, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNPR",
  "name": "Monopar Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNRO",
  "name": "Monro, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNSB",
  "name": "MainStreet Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNSBP",
  "name": "MainStreet Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNST",
  "name": "Monster Beverage Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNTK",
  "name": "Montauk Renewables, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNTL",
  "name": "Tema Neuroscience and Mental Health ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNTS",
  "name": "Momentus Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNTSW",
  "name": "Momentus Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNTX",
  "name": "Manitex International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNY",
  "name": "MoneyHero Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MNYWW",
  "name": "MoneyHero Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOB",
  "name": "Mobilicom Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOBBW",
  "name": "Mobilicom Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOBX",
  "name": "Mobix Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOBXW",
  "name": "Mobix Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MODD",
  "name": "Modular Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MODL",
  "name": "VictoryShares WestEnd U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MODV",
  "name": "ModivCare Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOFG",
  "name": "MidWestOne Financial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOGO",
  "name": "Mogo Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOLN",
  "name": "Molecular Partners AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOMO",
  "name": "Hello Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOND",
  "name": "Mondee Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOOD",
  "name": "Relative Sentiment Tactical Allocation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOR",
  "name": "MorphoSys AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MORF",
  "name": "Morphic Holding, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MORN",
  "name": "Morningstar, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MOVE",
  "name": "Movano Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MPAA",
  "name": "Motorcar Parts of America, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MPB",
  "name": "Mid Penn Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MPWR",
  "name": "Monolithic Power Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MQ",
  "name": "Marqeta, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRAI",
  "name": "Marpai, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRAM",
  "name": "Everspin Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRBK",
  "name": "Meridian Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRCC",
  "name": "Monroe Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRCY",
  "name": "Mercury Systems Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MREO",
  "name": "Mereo BioPharma Group plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRIN",
  "name": "Marin Software Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRKR",
  "name": "Marker Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRM",
  "name": "MEDIROM Healthcare Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRNA",
  "name": "Moderna, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRNO",
  "name": "Murano Global Investments PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRNOW",
  "name": "Murano Global Investments PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRNS",
  "name": "Marinus Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRSN",
  "name": "Mersana Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRTN",
  "name": "Marten Transport, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRUS",
  "name": "Merus N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRVI",
  "name": "Maravai LifeSciences Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRVL",
  "name": "Marvell Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MRX",
  "name": "Marex Group plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSAI",
  "name": "MultiSensor AI Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSAIW",
  "name": "MultiSensor AI Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSBI",
  "name": "Midland States Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSBIP",
  "name": "Midland States Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSEX",
  "name": "Middlesex Water Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSFD",
  "name": "Direxion Daily MSFT Bear 1X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSFL",
  "name": "GraniteShares 2x Long MSFT Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSFT",
  "name": "Microsoft Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSFU",
  "name": "Direxion Daily MSFT Bull 2X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSGM",
  "name": "Motorsport Games Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSS",
  "name": "Maison Solutions Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSSA",
  "name": "Metal Sky Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSSAR",
  "name": "Metal Sky Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSSAU",
  "name": "Metal Sky Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSSAW",
  "name": "Metal Sky Star Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MSTR",
  "name": "MicroStrategy Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTC",
  "name": "MMTec, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTCH",
  "name": "Match Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTEK",
  "name": "Maris",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTEKW",
  "name": "Maris",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTEM",
  "name": "Molecular Templates, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTEN",
  "name": "Mingteng International Corporation Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTEX",
  "name": "Mannatech, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTLS",
  "name": "Materialise NV ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTRX",
  "name": "Matrix Service Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTSI",
  "name": "MACOM Technology Solutions Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MTTR",
  "name": "Matterport, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MU",
  "name": "Micron Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MULN",
  "name": "Mullen Automotive, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MURA",
  "name": "Mural Oncology plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MVBF",
  "name": "MVB Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MVIS",
  "name": "MicroVision, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MVST",
  "name": "Microvast Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MVSTW",
  "name": "Microvast Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MXCT",
  "name": "MaxCyte, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MXL",
  "name": "MaxLinear, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYFW",
  "name": "First Western Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYGN",
  "name": "Myriad Genetics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYMD",
  "name": "MyMD Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYNA",
  "name": "Mynaric AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYNZ",
  "name": "Mainz Biomed N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYPS",
  "name": "PLAYSTUDIOS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYPSW",
  "name": "PLAYSTUDIOS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYRG",
  "name": "MYR Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "MYSZ",
  "name": "My Size, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NA",
  "name": "Nano Labs Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAAS",
  "name": "NaaS Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAII",
  "name": "Natural Alternatives International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAMS",
  "name": "NewAmsterdam Pharma Company N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAMSW",
  "name": "NewAmsterdam Pharma Company N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAOV",
  "name": "NanoVibronix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NARI",
  "name": "Inari Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NATH",
  "name": "Nathan's Famous, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NATR",
  "name": "Nature's Sunshine Products, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAUT",
  "name": "Nautilus Biotechnology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NAVI",
  "name": "Navient Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NB",
  "name": "NioCorp Developments Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBBK",
  "name": "NB Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBIX",
  "name": "Neurocrine Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBN",
  "name": "Northeast Bank ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBSE",
  "name": "NeuBase Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBST",
  "name": "Newbury Street Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBSTU",
  "name": "Newbury Street Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBSTW",
  "name": "Newbury Street Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBTB",
  "name": "NBT Bancorp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NBTX",
  "name": "Nanobiotix S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCI",
  "name": "Neo",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCMI",
  "name": "National CineMedia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCNA",
  "name": "NuCana plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCNC",
  "name": "noco",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCNCW",
  "name": "noco",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCNO",
  "name": "nCino, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCPB",
  "name": "Nuveen Core Plus Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCPL",
  "name": "Netcapital Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCPLW",
  "name": "Netcapital Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCRA",
  "name": "Nocera, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCSM",
  "name": "NCS Multistage Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NCTY",
  "name": "The9 Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NDAQ",
  "name": "Nasdaq, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NDLS",
  "name": "Noodles & Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NDRA",
  "name": "ENDRA Life Sciences Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NDSN",
  "name": "Nordson Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NECB",
  "name": "NorthEast Community Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEGG",
  "name": "Newegg Commerce, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEO",
  "name": "NeoGenomics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEOG",
  "name": "Neogen Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEON",
  "name": "Neonode Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEOV",
  "name": "NeoVolta Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEOVW",
  "name": "NeoVolta Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEPH",
  "name": "Nephros, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NERD",
  "name": "Roundhill Video Games ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NERV",
  "name": "Minerva Neurosciences, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NETD",
  "name": "Nabors Energy Transition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NETDU",
  "name": "Nabors Energy Transition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NETDW",
  "name": "Nabors Energy Transition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEWT",
  "name": "NewtekOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEWTI",
  "name": "NewtekOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEWTL",
  "name": "NewtekOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEWTZ",
  "name": "NewtekOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEWZ",
  "name": "StockSnips AI",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEXI",
  "name": "NexImmune, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEXN",
  "name": "Nexxen International Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NEXT",
  "name": "NextDecade Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NFBK",
  "name": "Northfield Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NFE",
  "name": "New Fortress Energy Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NFLX",
  "name": "Netflix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NFTY",
  "name": "First Trust India Nifty 50 Equal Weight ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NGNE",
  "name": "Neurogene Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NHTC",
  "name": "Natural Health Trends Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NICE",
  "name": "NICE Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NICK",
  "name": "Nicholas Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NIKL",
  "name": "Sprott Nickel Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NIOBW",
  "name": "NioCorp Developments Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NISN",
  "name": "NiSun Intl Enterprise Development Group Co, Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NITO",
  "name": "N2OFF, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NIU",
  "name": "Niu Technologies ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NIVF",
  "name": "NewGenIvf Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NIVFW",
  "name": "NewGenIvf Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NKGN",
  "name": "NKGen Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NKGNW",
  "name": "NKGen Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NKLA",
  "name": "Nikola Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NKSH",
  "name": "National Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NKTR",
  "name": "Nektar Therapeutics ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NKTX",
  "name": "Nkarta, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NLSP",
  "name": "NLS Pharmaceutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NLSPW",
  "name": "NLS Pharmaceutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMFC",
  "name": "New Mountain Finance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMFCZ",
  "name": "New Mountain Finance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMHI",
  "name": "Nature's Miracle Holding Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMHIW",
  "name": "Nature's Miracle Holding Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMIH",
  "name": "NMI Holdings Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMRA",
  "name": "Neumora Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMRK",
  "name": "Newmark Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NMTC",
  "name": "NeuroOne Medical Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NN",
  "name": "NextNav Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNAG",
  "name": "99 Acquisition Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNAGR",
  "name": "99 Acquisition Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNAGU",
  "name": "99 Acquisition Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNAGW",
  "name": "99 Acquisition Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNAVW",
  "name": "NextNav Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNBR",
  "name": "NN, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNDM",
  "name": "Nano Dimension Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNE",
  "name": "Nano Nuclear Energy Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NNOX",
  "name": "NANO",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NODK",
  "name": "NI Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NOTV",
  "name": "Inotiv, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NOVT",
  "name": "Novanta Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NOVV",
  "name": "Nova Vision Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NOVVR",
  "name": "Nova Vision Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NOVVU",
  "name": "Nova Vision Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NOVVW",
  "name": "Nova Vision Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NPAB",
  "name": "New Providence Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NPABU",
  "name": "New Providence Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NPABW",
  "name": "New Providence Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NPCE",
  "name": "Neuropace, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NPFI",
  "name": "Nuveen Preferred and Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRBO",
  "name": "NeuroBo Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRC",
  "name": "National Research Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRDS",
  "name": "NerdWallet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRES",
  "name": "Xtrackers RREEF Global Natural Resources ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRIM",
  "name": "Northrim BanCorp Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRIX",
  "name": "Nurix Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRSN",
  "name": "NeuroSense Therapeutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRSNW",
  "name": "NeuroSense Therapeutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRXP",
  "name": "NRX Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NRXPW",
  "name": "NRX Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSCR",
  "name": "Nuveen Sustainable Core ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSI",
  "name": "National Security Emerging Markets Index ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSIT",
  "name": "Insight Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSPR",
  "name": "InspireMD Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSSC",
  "name": "NAPCO Security Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSTS",
  "name": "NSTS Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NSYS",
  "name": "Nortech Systems Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTAP",
  "name": "NetApp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTBL",
  "name": "Notable Labs, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTCT",
  "name": "NetScout Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTES",
  "name": "NetEase, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTGR",
  "name": "NETGEAR, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTIC",
  "name": "Northern Technologies International Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTLA",
  "name": "Intellia Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTNX",
  "name": "Nutanix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTRA",
  "name": "Natera, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTRB",
  "name": "Nutriband Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTRBW",
  "name": "Nutriband Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTRP",
  "name": "NextTrip, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTRS",
  "name": "Northern Trust Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTRSO",
  "name": "Northern Trust Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTWK",
  "name": "NETSOL Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NTZG",
  "name": "Nuveen Global Net Zero Transition ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUKK",
  "name": "Nukkleus Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUKKW",
  "name": "Nukkleus Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NURO",
  "name": "NeuroMetrix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUSB",
  "name": "Nuveen Ultra Short Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUTX",
  "name": "Nutex Health Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUVL",
  "name": "Nuvalent, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUVO",
  "name": "Holdco Nuvo Group D.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUVOW",
  "name": "Holdco Nuvo Group D.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUWE",
  "name": "Nuwellis, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NUZE",
  "name": "NuZee, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVAC",
  "name": "NorthView Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVACR",
  "name": "NorthView Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVACW",
  "name": "NorthView Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVAX",
  "name": "Novavax, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVCR",
  "name": "NovoCure Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVCT",
  "name": "Nuvectis Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVD",
  "name": "GraniteShares 2x Short NVDA Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVDA",
  "name": "NVIDIA Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVDD",
  "name": "Direxion Daily NVDA Bear 1X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVDL",
  "name": "GraniteShares 2x Long NVDA Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVDS",
  "name": "AXS 1.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVDU",
  "name": "Direxion Daily NVDA Bull 2X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVEC",
  "name": "NVE Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVEE",
  "name": "NV5 Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVEI",
  "name": "Nuvei Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVFY",
  "name": "Nova Lifestyle, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVMI",
  "name": "Nova Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVNI",
  "name": "Nvni Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVNIW",
  "name": "Nvni Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVNO",
  "name": "enVVeno Medical Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVOS",
  "name": "Novo Integrated Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVTS",
  "name": "Navitas Semiconductor Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVVE",
  "name": "Nuvve Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVVEW",
  "name": "Nuvve Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NVX",
  "name": "NOVONIX Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWBI",
  "name": "Northwest Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWE",
  "name": "NorthWestern Energy Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWFL",
  "name": "Norwood Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWGL",
  "name": "Nature Wood Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWL",
  "name": "Newell Brands Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWLI",
  "name": "National Western Life Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWPX",
  "name": "Northwest Pipe Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWS",
  "name": "News Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWSA",
  "name": "News Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWTN",
  "name": "NWTN Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NWTNW",
  "name": "NWTN Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXGL",
  "name": "NexGel, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXGLW",
  "name": "NexGel, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXL",
  "name": "Nexalin Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXLIW",
  "name": "Nexalin Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXPI",
  "name": "NXP Semiconductors N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXPL",
  "name": "NextPlat Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXPLW",
  "name": "NextPlat Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXST",
  "name": "Nexstar Media Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXT",
  "name": "Nextracker Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXTC",
  "name": "NextCure, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXTG",
  "name": "First Trust Indxx NextG ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXTT",
  "name": "Next Technology Holding Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NXU",
  "name": "Nxu, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYAX",
  "name": "Nayax Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYMT",
  "name": "New York Mortgage Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYMTL",
  "name": "New York Mortgage Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYMTM",
  "name": "New York Mortgage Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYMTN",
  "name": "New York Mortgage Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYMTZ",
  "name": "New York Mortgage Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NYXH",
  "name": "Nyxoah SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NZAC",
  "name": "SPDR MSCI ACWI Climate Paris Aligned ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "NZUS",
  "name": "SPDR MSCI USA Climate Paris Aligned ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OABI",
  "name": "OmniAb, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OABIW",
  "name": "OmniAb, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OAKU",
  "name": "Oak Woods Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OAKUR",
  "name": "Oak Woods Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OAKUU",
  "name": "Oak Woods Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OAKUW",
  "name": "Oak Woods Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OB",
  "name": "Outbrain Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OBIL",
  "name": "US Treasury 12 Month Bill ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OBIO",
  "name": "Orchestra BioMed Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OBLG",
  "name": "Oblong Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OBT",
  "name": "Orange County Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCAX",
  "name": "OCA Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCAXU",
  "name": "OCA Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCAXW",
  "name": "OCA Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCC",
  "name": "Optical Cable Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCCI",
  "name": "OFS Credit Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCCIN",
  "name": "OFS Credit Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCCIO",
  "name": "OFS Credit Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCEA",
  "name": "Ocean Biomedical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCEAW",
  "name": "Ocean Biomedical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCFC",
  "name": "OceanFirst Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCFCP",
  "name": "OceanFirst Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCG",
  "name": "Oriental Culture Holding LTD ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCGN",
  "name": "Ocugen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCS",
  "name": "Oculis Holding AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCSAW",
  "name": "Oculis Holding AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCSL",
  "name": "Oaktree Specialty Lending Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCTO",
  "name": "Eightco Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCUL",
  "name": "Ocular Therapeutix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCUP",
  "name": "Ocuphire Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OCX",
  "name": "Oncocyte Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ODD",
  "name": "ODDITY Tech Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ODDS",
  "name": "Pacer BlueStar Digital Entertainment ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ODFL",
  "name": "Old Dominion Freight Line, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ODP",
  "name": "The ODP Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ODVWZ",
  "name": "Osisko Development Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OESX",
  "name": "Orion Energy Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OFIX",
  "name": "Orthofix Medical Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OFLX",
  "name": "Omega Flex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OFS",
  "name": "OFS Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OFSSH",
  "name": "OFS Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OGI",
  "name": "Organigram Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OKTA",
  "name": "Okta, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OKYO",
  "name": "OKYO Pharma Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OLB",
  "name": "The OLB Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OLED",
  "name": "Universal Display Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OLK",
  "name": "Olink Holding AB (publ) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OLLI",
  "name": "Ollie's Bargain Outlet Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OLMA",
  "name": "Olema Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OLPX",
  "name": "Olaplex Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OM",
  "name": "Outset Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMAB",
  "name": "Grupo Aeroportuario del Centro Norte S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMCL",
  "name": "Omnicell, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMER",
  "name": "Omeros Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMEX",
  "name": "Odyssey Marine Exploration, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMGA",
  "name": "Omega Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMH",
  "name": "Ohmyhome Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OMIC",
  "name": "Singular Genomics Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ON",
  "name": "ON Semiconductor Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONB",
  "name": "Old National Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONBPO",
  "name": "Old National Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONBPP",
  "name": "Old National Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONCO",
  "name": "Onconetix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONCT",
  "name": "Oncternal Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONCY",
  "name": "Oncolytics Biotech Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONDS",
  "name": "Ondas Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONEQ",
  "name": "Fidelity Nasdaq Composite Index ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONEW",
  "name": "OneWater Marine Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONFO",
  "name": "Onfolio Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONFOW",
  "name": "Onfolio Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONMD",
  "name": "OneMedNet Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONMDW",
  "name": "OneMedNet Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONVO",
  "name": "Organovo Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONYX",
  "name": "Onyx Acquisition Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONYXU",
  "name": "Onyx Acquisition Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ONYXW",
  "name": "Onyx Acquisition Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OP",
  "name": "OceanPal Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPAL",
  "name": "OPAL Fuels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPBK",
  "name": "OP Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPCH",
  "name": "Option Care Health, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPEN",
  "name": "Opendoor Technologies Inc  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPGN",
  "name": "OpGen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPHC",
  "name": "OptimumBank Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPI",
  "name": "Office Properties Income Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPINL",
  "name": "Office Properties Income Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPK",
  "name": "Opko Health, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPOF",
  "name": "Old Point Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPRA",
  "name": "Opera Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPRT",
  "name": "Oportun Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPRX",
  "name": "OptimizeRx Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPT",
  "name": "Opthea Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPTN",
  "name": "OptiNose, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPTX",
  "name": "Syntec Optics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPTXW",
  "name": "Syntec Optics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPTZ",
  "name": "Optimize Strategy Index ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OPXS",
  "name": "Optex Systems Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORGN",
  "name": "Origin Materials, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORGNW",
  "name": "Origin Materials, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORGO",
  "name": "Organogenesis Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORGS",
  "name": "Orgenesis Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORIC",
  "name": "Oric Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORLY",
  "name": "O'Reilly Automotive, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORMP",
  "name": "Oramed Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ORRF",
  "name": "Orrstown Financial Services Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OSBC",
  "name": "Old Second Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OSIS",
  "name": "OSI Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OSPN",
  "name": "OneSpan Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OSS",
  "name": "One Stop Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OST",
  "name": "Ostin Technology Group Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OSUR",
  "name": "OraSure Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OSW",
  "name": "OneSpaWorld Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OTEX",
  "name": "Open Text Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OTLK",
  "name": "Outlook Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OTLY",
  "name": "Oatly Group AB ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OTRK",
  "name": "Ontrak, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OTTR",
  "name": "Otter Tail Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OVBC",
  "name": "Ohio Valley Banc Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OVID",
  "name": "Ovid Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OVLY",
  "name": "Oak Valley Bancorp (CA) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXBR",
  "name": "Oxbridge Re Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXBRW",
  "name": "Oxbridge Re Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLC",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLCL",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLCM",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLCN",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLCO",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLCP",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXLCZ",
  "name": "Oxford Lane Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXSQ",
  "name": "Oxford Square Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXSQG",
  "name": "Oxford Square Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OXSQZ",
  "name": "Oxford Square Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OZK",
  "name": "Bank OZK ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "OZKAP",
  "name": "Bank OZK ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAA",
  "name": "Plains All American Pipeline, L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PABD",
  "name": "iShares Paris",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PABU",
  "name": "iShares Paris",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PACB",
  "name": "Pacific Biosciences of California, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAGP",
  "name": "Plains GP Holdings, L.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAHC",
  "name": "Phibro Animal Health Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PALI",
  "name": "Palisade Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PALT",
  "name": "Paltalk, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PANL",
  "name": "Pangaea Logistics Solutions Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PANW",
  "name": "Palo Alto Networks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PARA",
  "name": "Paramount Global ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PARAA",
  "name": "Paramount Global ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PASG",
  "name": "Passage Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PATK",
  "name": "Patrick Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAVM",
  "name": "PAVmed Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAVMZ",
  "name": "PAVmed Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAVS",
  "name": "Paranovus Entertainment Technology Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAX",
  "name": "Patria Investments Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAYO",
  "name": "Payoneer Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAYOW",
  "name": "Payoneer Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAYS",
  "name": "Paysign, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PAYX",
  "name": "Paychex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBBK",
  "name": "PB Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBFS",
  "name": "Pioneer Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBHC",
  "name": "Pathfinder Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBM",
  "name": "Psyence Biomedical Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBMWW",
  "name": "Psyence Biomedical Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBPB",
  "name": "Potbelly Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PBYI",
  "name": "Puma Biotechnology Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCAR",
  "name": "PACCAR Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCB",
  "name": "PCB Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCH",
  "name": "PotlatchDeltic Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCRX",
  "name": "Pacira BioSciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCSA",
  "name": "Processa Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCT",
  "name": "PureCycle Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCTTU",
  "name": "PureCycle Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCTTW",
  "name": "PureCycle Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCTY",
  "name": "Paylocity Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCVX",
  "name": "Vaxcyte, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PCYO",
  "name": "Pure Cycle Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDBA",
  "name": "Invesco Agriculture Commodity Strategy No K",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDBC",
  "name": "Invesco Optimum Yield Diversified Commodity Strategy No K",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDCO",
  "name": "Patterson Companies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDD",
  "name": "PDD Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDEX",
  "name": "Pro",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDFS",
  "name": "PDF Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDLB",
  "name": "Ponce Financial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDP",
  "name": "Invesco Dorsey Wright Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDSB",
  "name": "PDS Biotechnology Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDYN",
  "name": "Palladyne AI Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PDYNW",
  "name": "Palladyne AI Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEBK",
  "name": "Peoples Bancorp of North Carolina, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEBO",
  "name": "Peoples Bancorp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PECO",
  "name": "Phillips Edison & Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEGA",
  "name": "Pegasystems Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEGR",
  "name": "Project Energy Reimagined Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEGRU",
  "name": "Project Energy Reimagined Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEGRW",
  "name": "Project Energy Reimagined Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEGY",
  "name": "Pineapple Energy Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PENN",
  "name": "PENN Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEP",
  "name": "PepsiCo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEPG",
  "name": "PepGen Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PERI",
  "name": "Perion Network Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PESI",
  "name": "Perma",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PET",
  "name": "Wag! Group Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PETQ",
  "name": "PetIQ, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PETS",
  "name": "PetMed Express, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PETWW",
  "name": "Wag! Group Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PETZ",
  "name": "TDH Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEV",
  "name": "Phoenix Motor Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEY",
  "name": "Invesco High Yield Equity Dividend Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PEZ",
  "name": "Invesco Dorsey Wright Consumer Cyclicals Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFBC",
  "name": "Preferred Bank ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFC",
  "name": "Premier Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFF",
  "name": "iShares Preferred and Income Securities ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFG",
  "name": "Principal Financial Group Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFI",
  "name": "Invesco Dorsey Wright Financial Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFIE",
  "name": "Profire Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFIS",
  "name": "Peoples Financial Services Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFM",
  "name": "Invesco Dividend Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFMT",
  "name": "Performant Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFTA",
  "name": "Perception Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFTAU",
  "name": "Perception Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFTAW",
  "name": "Perception Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFX",
  "name": "PhenixFIN Corporation  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PFXNZ",
  "name": "PhenixFIN Corporation  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PGC",
  "name": "Peapack",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PGEN",
  "name": "Precigen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PGJ",
  "name": "Invesco Golden Dragon China ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PGNY",
  "name": "Progyny, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PGY",
  "name": "Pagaya Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PGYWW",
  "name": "Pagaya Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PHAR",
  "name": "Pharming Group N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PHAT",
  "name": "Phathom Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PHIO",
  "name": "Phio Pharmaceuticals Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PHO",
  "name": "Invesco Water Resources ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PHUN",
  "name": "Phunware, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PHVS",
  "name": "Pharvaris N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PI",
  "name": "Impinj, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PID",
  "name": "Invesco International Dividend Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIE",
  "name": "Invesco Dorsey Wright Emerging Markets Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIII",
  "name": "P3 Health Partners Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIIIW",
  "name": "P3 Health Partners Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIK",
  "name": "Kidpik Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PINC",
  "name": "Premier, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIO",
  "name": "Invesco Global Water ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIRS",
  "name": "Pieris Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIXY",
  "name": "ShiftPixy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PIZ",
  "name": "Invesco Dorsey Wright Developed Markets Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PKBK",
  "name": "Parke Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PKOH",
  "name": "Park",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PKW",
  "name": "Invesco BuyBack Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLAB",
  "name": "Photronics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLAO",
  "name": "Patria Latin American Opportunity Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLAOU",
  "name": "Patria Latin American Opportunity Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLAOW",
  "name": "Patria Latin American Opportunity Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLAY",
  "name": "Dave & Buster's Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLBC",
  "name": "Plumas Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLBY",
  "name": "PLBY Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLCE",
  "name": "Children's Place, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLL",
  "name": "Piedmont Lithium Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMI",
  "name": "Plum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMIU",
  "name": "Plum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMIW",
  "name": "Plum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMJ",
  "name": "Plum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMJU",
  "name": "Plum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMJW",
  "name": "Plum Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLMR",
  "name": "Palomar Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLPC",
  "name": "Preformed Line Products Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLRX",
  "name": "Pliant Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLSE",
  "name": "Pulse Biosciences, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLTK",
  "name": "Playtika Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLTN",
  "name": "Plutonian Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLTNR",
  "name": "Plutonian Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLTNU",
  "name": "Plutonian Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLTNW",
  "name": "Plutonian Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLUG",
  "name": "Plug Power, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLUR",
  "name": "Pluri Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLUS",
  "name": "ePlus inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLXS",
  "name": "Plexus Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PLYA",
  "name": "Playa Hotels & Resorts N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMCB",
  "name": "PharmaCyte  Biotech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMD",
  "name": "Psychemedics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMEC",
  "name": "Primech Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMGM",
  "name": "Priveterra Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMGMU",
  "name": "Priveterra Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMGMW",
  "name": "Priveterra Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMN",
  "name": "ProMIS Neurosciences Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMTS",
  "name": "CPI Card Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PMVP",
  "name": "PMV Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PNBK",
  "name": "Patriot National Bancorp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PNFP",
  "name": "Pinnacle Financial Partners, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PNFPP",
  "name": "Pinnacle Financial Partners, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PNQI",
  "name": "Invesco Nasdaq Internet ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PNRG",
  "name": "PrimeEnergy Resources Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PNTG",
  "name": "The Pennant Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POAI",
  "name": "Predictive Oncology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POCI",
  "name": "Precision Optics Corporation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PODC",
  "name": "PodcastOne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PODD",
  "name": "Insulet Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POET",
  "name": "POET Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POLA",
  "name": "Polar Power, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POOL",
  "name": "Pool Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POWI",
  "name": "Power Integrations, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POWL",
  "name": "Powell Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POWW",
  "name": "AMMO, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "POWWP",
  "name": "AMMO, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPBI",
  "name": "Pacific Premier Bancorp Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPBT",
  "name": "Purple Biotech Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPC",
  "name": "Pilgrim's Pride Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPH",
  "name": "VanEck Pharmaceutical ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPIH",
  "name": "Perma",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPSI",
  "name": "Pioneer Power Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPTA",
  "name": "Perpetua Resources Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPYA",
  "name": "Papaya Growth Opportunity Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPYAU",
  "name": "Papaya Growth Opportunity Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PPYAW",
  "name": "Papaya Growth Opportunity Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRAA",
  "name": "PRA Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRAX",
  "name": "Praxis Precision Medicines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRCH",
  "name": "Porch Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRCT",
  "name": "PROCEPT BioRobotics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRDO",
  "name": "Perdoceo Education Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRE",
  "name": "Prenetics Global Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRENW",
  "name": "Prenetics Global Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRFT",
  "name": "Perficient, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRFX",
  "name": "PainReform Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRFZ",
  "name": "Invesco FTSE RAFI US 1500 Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRGS",
  "name": "Progress Software Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRLD",
  "name": "Prelude Therapeutics Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRLH",
  "name": "Pearl Holdings Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRLHU",
  "name": "Pearl Holdings Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRLHW",
  "name": "Pearl Holdings Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRME",
  "name": "Prime Medicine, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRN",
  "name": "Invesco Dorsey Wright Industrials Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PROC",
  "name": "Procaps Group, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PROCW",
  "name": "Procaps Group, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PROF",
  "name": "Profound Medical Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PROK",
  "name": "ProKidney Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PROP",
  "name": "Prairie Operating Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PROV",
  "name": "Provident Financial Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRPH",
  "name": "ProPhase Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRPL",
  "name": "Purple Innovation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRPO",
  "name": "Precipio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRQR",
  "name": "ProQR Therapeutics N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRSO",
  "name": "Peraso Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRST",
  "name": "Presto Automation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRSTW",
  "name": "Presto Automation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRTA",
  "name": "Prothena Corporation plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRTC",
  "name": "PureTech Health plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRTG",
  "name": "Portage Biotech Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRTH",
  "name": "Priority Technology Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRTS",
  "name": "CarParts.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRVA",
  "name": "Privia Health Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PRZO",
  "name": "ParaZero Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSC",
  "name": "Principal U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCC",
  "name": "Invesco S&P SmallCap Consumer Staples ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCD",
  "name": "Invesco S&P SmallCap Consumer Discretionary ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCE",
  "name": "Invesco S&P SmallCap Energy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCF",
  "name": "Invesco S&P SmallCap Financials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCH",
  "name": "Invesco S&P SmallCap Health Care ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCI",
  "name": "Invesco S&P SmallCap Industrials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCM",
  "name": "Invesco S&P SmallCap Materials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCT",
  "name": "Invesco S&P SmallCap Information Technology ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSCU",
  "name": "Invesco S&P SmallCap Utilities & Communication Services ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSEC",
  "name": "Prospect Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSET",
  "name": "Principal Quality ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSHG",
  "name": "Performance Shipping Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSL",
  "name": "Invesco Dorsey Wright Consumer Staples Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSMT",
  "name": "PriceSmart, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSNL",
  "name": "Personalis, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSNY",
  "name": "Polestar Automotive Holding UK Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSNYW",
  "name": "Polestar Automotive Holding UK Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSTR",
  "name": "PeakShares Sector Rotation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSTV",
  "name": "PLUS THERAPEUTICS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSTX",
  "name": "Poseida Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PSWD",
  "name": "Xtrackers Cybersecurity Select Equity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PT",
  "name": "Pintec Technology Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTC",
  "name": "PTC Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTCT",
  "name": "PTC Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTEC",
  "name": "Global X PropTech ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTEN",
  "name": "Patterson",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTF",
  "name": "Invesco Dorsey Wright Technology Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTGX",
  "name": "Protagonist Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTH",
  "name": "Invesco Dorsey Wright Healthcare Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTIX",
  "name": "Protagenic Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTIXW",
  "name": "Protagenic Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTLO",
  "name": "Portillo's Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTMN",
  "name": "Portman Ridge Finance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTNQ",
  "name": "Pacer Trendpilot 100 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTON",
  "name": "Peloton Interactive, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTPI",
  "name": "Petros Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTSI",
  "name": "P.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTVE",
  "name": "Pactiv Evergreen Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTWO",
  "name": "Pono Capital Two, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTWOU",
  "name": "Pono Capital Two, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PTWOW",
  "name": "Pono Capital Two, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PUBM",
  "name": "PubMatic, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PUCK",
  "name": "Goal Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PUCKU",
  "name": "Goal Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PUCKW",
  "name": "Goal Acquisitions Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PUI",
  "name": "Invesco Dorsey Wright Utilities Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PULM",
  "name": "Pulmatrix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PVBC",
  "name": "Provident Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWFL",
  "name": "PowerFleet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWM",
  "name": "Prestige Wealth Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWOD",
  "name": "Penns Woods Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWP",
  "name": "Perella Weinberg Partners ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWUP",
  "name": "PowerUp Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWUPU",
  "name": "PowerUp Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PWUPW",
  "name": "PowerUp Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PXDT",
  "name": "Pixie Dust Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PXI",
  "name": "Invesco Dorsey Wright Energy Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PXLW",
  "name": "Pixelworks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PXS",
  "name": "Pyxis Tankers Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PXSAP",
  "name": "Pyxis Tankers Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PXSAW",
  "name": "Pyxis Tankers Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PY",
  "name": "Principal Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PYCR",
  "name": "Paycor HCM, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PYPD",
  "name": "PolyPid Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PYPL",
  "name": "PayPal Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PYXS",
  "name": "Pyxis Oncology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PYZ",
  "name": "Invesco Dorsey Wright Basic Materials Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "PZZA",
  "name": "Papa John's International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QABA",
  "name": "First Trust NASDAQ ABA Community Bank Index Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QAT",
  "name": "iShares MSCI Qatar ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QCLN",
  "name": "First Trust NASDAQ Clean Edge Green Energy Index Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QCLR",
  "name": "Global X NASDAQ 100 Collar 95",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QCOM",
  "name": "QUALCOMM Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QCRH",
  "name": "QCR Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QDEL",
  "name": "QuidelOrtho Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QDRO",
  "name": "Quadro Acquisition One Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QDROU",
  "name": "Quadro Acquisition One Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QDROW",
  "name": "Quadro Acquisition One Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QETA",
  "name": "Quetta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QETAR",
  "name": "Quetta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QETAU",
  "name": "Quetta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QFIN",
  "name": "Qifu Technology, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QH",
  "name": "Quhuo Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QIPT",
  "name": "Quipt Home Medical Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QIWI",
  "name": "QIWI plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QLGN",
  "name": "Qualigen Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QLI",
  "name": "Qilian International Holding Group Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QLYS",
  "name": "Qualys, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QMCO",
  "name": "Quantum Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QMID",
  "name": "WisdomTree U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QMOM",
  "name": "Alpha Architect U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QNCX",
  "name": "Quince Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QNRX",
  "name": "Quoin Pharmaceuticals, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QNST",
  "name": "QuinStreet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QOMO",
  "name": "Qomolangma Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QOMOR",
  "name": "Qomolangma Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QOMOU",
  "name": "Qomolangma Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QOMOW",
  "name": "Qomolangma Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QOWZ",
  "name": "Invesco Nasdaq Free Cash Flow Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQEW",
  "name": "First Trust NASDAQ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQJG",
  "name": "Invesco ESG NASDAQ Next Gen 100 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQMG",
  "name": "Invesco ESG NASDAQ 100 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQ",
  "name": "Invesco QQQ Trust, Series 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQA",
  "name": "ProShares Nasdaq",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQE",
  "name": "Direxion NASDAQ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQI",
  "name": "NEOS Nasdaq 100 High Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQJ",
  "name": "Invesco NASDAQ Next Gen 100 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQM",
  "name": "Invesco NASDAQ 100 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQN",
  "name": "VictoryShares Nasdaq Next 50 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQS",
  "name": "Invesco NASDAQ Future Gen 200 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQX",
  "name": "Nuveen NASDAQ 100 Dynamic Overwrite Fund ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQQY",
  "name": "Defiance Nasdaq 100 Enhanced Options Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QQXT",
  "name": "First Trust NASDAQ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QRHC",
  "name": "Quest Resource Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QRMI",
  "name": "Global X NASDAQ 100 Risk Managed Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QRTEA",
  "name": "Qurate Retail, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QRTEB",
  "name": "Qurate Retail, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QRTEP",
  "name": "Qurate Retail, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QRVO",
  "name": "Qorvo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QSG",
  "name": "QuantaSing Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QSI",
  "name": "Quantum",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QSIAW",
  "name": "Quantum",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QSML",
  "name": "WisdomTree U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QTEC",
  "name": "First Trust NASDAQ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QTI",
  "name": "QT Imaging Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QTR",
  "name": "Global X NASDAQ 100 Tail Risk ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QTRX",
  "name": "Quanterix Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QTTB",
  "name": "Q32 Bio Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QUBT",
  "name": "Quantum Computing Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QUIK",
  "name": "QuickLogic Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QURE",
  "name": "uniQure N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QVAL",
  "name": "Alpha Architect U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QYLD",
  "name": "Global X NASDAQ 100 Covered Call ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QYLE",
  "name": "Global X Nasdaq 100 ESG Covered Call ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "QYLG",
  "name": "Global X Nasdaq 100 Covered Call & Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RAIL",
  "name": "Freightcar America, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RAND",
  "name": "Rand Capital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RANI",
  "name": "Rani Therapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RAPT",
  "name": "RAPT Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RARE",
  "name": "Ultragenyx Pharmaceutical Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RAVE",
  "name": "Rave Restaurant Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RAYA",
  "name": "Erayak Power Solution Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RAYS",
  "name": "Global X Solar ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RBB",
  "name": "RBB Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RBBN",
  "name": "Ribbon Communications Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RBCAA",
  "name": "Republic Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RBKB",
  "name": "Rhinebeck Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCAT",
  "name": "Red Cat Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCEL",
  "name": "Avita Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCKT",
  "name": "Rocket Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCKTW",
  "name": "Rocket Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCKY",
  "name": "Rocky Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCM",
  "name": "R1 RCM Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCMT",
  "name": "RCM Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCON",
  "name": "Recon Technology, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCRT",
  "name": "Recruiter.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RCRTW",
  "name": "Recruiter.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDCM",
  "name": "Radcom Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDFN",
  "name": "Redfin Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDHL",
  "name": "Redhill Biopharma Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDI",
  "name": "Reading International Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDIB",
  "name": "Reading International Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDNT",
  "name": "RadNet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDUS",
  "name": "Radius Recycling, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDVT",
  "name": "Red Violet, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDVY",
  "name": "First Trust Rising Dividend Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDWR",
  "name": "Radware Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDZN",
  "name": "Roadzen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RDZNW",
  "name": "Roadzen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REAI",
  "name": "Intelligent Real Estate ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REAL",
  "name": "The RealReal, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REAX",
  "name": "The Real Brokerage, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REBN",
  "name": "Reborn Coffee, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REE",
  "name": "REE Automotive Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REFI",
  "name": "Chicago Atlantic Real Estate Finance, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REFR",
  "name": "Research Frontiers Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REG",
  "name": "Regency Centers Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REGCO",
  "name": "Regency Centers Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REGCP",
  "name": "Regency Centers Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REGN",
  "name": "Regeneron Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REIT",
  "name": "ALPS Active REIT ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REKR",
  "name": "Rekor Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RELI",
  "name": "Reliance Global Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RELIW",
  "name": "Reliance Global Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RELL",
  "name": "Richardson Electronics, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RELY",
  "name": "Remitly Global, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RENB",
  "name": "Renovaro Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RENE",
  "name": "Cartesian Growth Corporation II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RENEU",
  "name": "Cartesian Growth Corporation II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RENEW",
  "name": "Cartesian Growth Corporation II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RENT",
  "name": "Rent the Runway, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REPL",
  "name": "Replimune Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RETO",
  "name": "ReTo Eco",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REVB",
  "name": "Revelation Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REVBW",
  "name": "Revelation Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "REYN",
  "name": "Reynolds Consumer Products Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFAC",
  "name": "RF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFACR",
  "name": "RF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFACU",
  "name": "RF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFACW",
  "name": "RF Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFDI",
  "name": "First Trust RiverFront Dynamic Developed International ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFEM",
  "name": "First Trust RiverFront Dynamic Emerging Markets ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFEU",
  "name": "First Trust RiverFront Dynamic Europe ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RFIL",
  "name": "RF Industries, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGC",
  "name": "Regencell Bioscience Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGCO",
  "name": "RGC Resources Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGEN",
  "name": "Repligen Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGF",
  "name": "The Real Good Food Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGLD",
  "name": "Royal Gold, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGLS",
  "name": "Regulus Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGNX",
  "name": "REGENXBIO Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGP",
  "name": "Resources Connection, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGS",
  "name": "Regis Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGTI",
  "name": "Rigetti Computing, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RGTIW",
  "name": "Rigetti Computing, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RICK",
  "name": "RCI Hospitality Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RIGL",
  "name": "Rigel Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILY",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYG",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYK",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYL",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYM",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYN",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYO",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYP",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYT",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RILYZ",
  "name": "B.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RING",
  "name": "iShares MSCI Global Gold Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RIOT",
  "name": "Riot Platforms, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RIVN",
  "name": "Rivian Automotive, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RKDA",
  "name": "Arcadia Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RKLB",
  "name": "Rocket Lab USA, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RLAY",
  "name": "Relay Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RLMD",
  "name": "Relmada Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RLYB",
  "name": "Rallybio Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMBI",
  "name": "Richmond Mutual Bancorporation, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMBL",
  "name": "RumbleOn, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMBS",
  "name": "Rambus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMCF",
  "name": "Rocky Mountain Chocolate Factory, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMCO",
  "name": "Royalty Management Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMCOW",
  "name": "Royalty Management Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMNI",
  "name": "Rimini Street, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMR",
  "name": "The RMR Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RMTI",
  "name": "Rockwell Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNA",
  "name": "Avidity Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNAC",
  "name": "Cartesian Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNAZ",
  "name": "TransCode Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNEM",
  "name": "Emerging Markets Equity Select ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNEW",
  "name": "VanEck Green Infrastructure ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNLX",
  "name": "Renalytix plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNMC",
  "name": "Mid Cap US Equity Select ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNRG",
  "name": "Global X Renewable Energy Producers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNSC",
  "name": "Small Cap US Equity Select ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNW",
  "name": "ReNew Energy Global plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNWWW",
  "name": "ReNew Energy Global plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RNXT",
  "name": "RenovoRx, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROAD",
  "name": "Construction Partners, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROBT",
  "name": "First Trust Nasdaq Artificial Intelligence and Robotics ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROCK",
  "name": "Gibraltar Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROCL",
  "name": "Roth CH Acquisition V Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROCLU",
  "name": "Roth CH Acquisition V Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROCLW",
  "name": "Roth CH Acquisition V Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROE",
  "name": "Astoria US Equal Weight Quality Kings ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROIC",
  "name": "Retail Opportunity Investments Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROIV",
  "name": "Roivant Sciences Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROKU",
  "name": "Roku, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROMA",
  "name": "Roma Green Finance Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROOT",
  "name": "Root, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROP",
  "name": "Roper Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ROST",
  "name": "Ross Stores, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RPAY",
  "name": "Repay Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RPD",
  "name": "Rapid7, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RPHM",
  "name": "Reneo Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RPID",
  "name": "Rapid Micro Biosystems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RPRX",
  "name": "Royalty Pharma plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RPTX",
  "name": "Repare Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RR",
  "name": "Richtech Robotics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RRBI",
  "name": "Red River Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RRGB",
  "name": "Red Robin Gourmet Burgers, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RRR",
  "name": "Red Rock Resorts, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RSLS",
  "name": "ReShape Lifesciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RSSS",
  "name": "Research Solutions, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RSVR",
  "name": "Reservoir Media, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RSVRW",
  "name": "Reservoir Media, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RTC",
  "name": "Baijiayun Group Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RTH",
  "name": "VanEck Retail ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RUM",
  "name": "Rumble Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RUMBW",
  "name": "Rumble Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RUN",
  "name": "Sunrun Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RUNN",
  "name": "Running Oak Efficient Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RUSHA",
  "name": "Rush Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RUSHB",
  "name": "Rush Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVMD",
  "name": "Revolution Medicines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVMDW",
  "name": "Revolution Medicines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVNC",
  "name": "Revance Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVPH",
  "name": "Reviva Pharmaceuticals Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVPHW",
  "name": "Reviva Pharmaceuticals Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVSB",
  "name": "Riverview Bancorp Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVSN",
  "name": "Rail Vision Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVSNW",
  "name": "Rail Vision Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RVYL",
  "name": "Ryvyl Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWAY",
  "name": "Runway Growth Finance Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWAYL",
  "name": "Runway Growth Finance Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWAYZ",
  "name": "Runway Growth Finance Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWOD",
  "name": "Redwoods Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWODR",
  "name": "Redwoods Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWODU",
  "name": "Redwoods Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RWODW",
  "name": "Redwoods Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RXRX",
  "name": "Recursion Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RXST",
  "name": "RxSight, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RXT",
  "name": "Rackspace Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RYAAY",
  "name": "Ryanair Holdings plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RYTM",
  "name": "Rhythm Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "RZLT",
  "name": "Rezolute, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SABR",
  "name": "Sabre Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SABS",
  "name": "SAB Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SABSW",
  "name": "SAB Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAFT",
  "name": "Safety Insurance Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAGE",
  "name": "Sage Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAI",
  "name": "SAI.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAIA",
  "name": "Saia, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAIC",
  "name": "Science Applications International Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAITW",
  "name": "SAI.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAMG",
  "name": "Silvercrest Asset Management Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SANA",
  "name": "Sana Biotechnology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SANG",
  "name": "Sangoma Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SANM",
  "name": "Sanmina Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SANW",
  "name": "S&W Seed Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SARK",
  "name": "AXS Short Innovation Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SASR",
  "name": "Sandy Spring Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SATL",
  "name": "Satellogic Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SATLW",
  "name": "Satellogic Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SATS",
  "name": "EchoStar Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SAVA",
  "name": "Cassava Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBAC",
  "name": "SBA Communications Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBCF",
  "name": "Seacoast Banking Corporation of Florida ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBET",
  "name": "SharpLink Gaming, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBFG",
  "name": "SB Financial Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBFM",
  "name": "Sunshine Biopharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBFMW",
  "name": "Sunshine Biopharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBGI",
  "name": "Sinclair, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBLK",
  "name": "Star Bulk Carriers Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBRA",
  "name": "Sabra Health Care REIT, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBSI",
  "name": "Southside Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBT",
  "name": "Sterling Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SBUX",
  "name": "Starbucks Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCHL",
  "name": "Scholastic Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCKT",
  "name": "Socket Mobile, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCLX",
  "name": "Scilex Holding Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCLXW",
  "name": "Scilex Holding Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCNI",
  "name": "Scinai Immunotherapeutics Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCOR",
  "name": "comScore, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCPH",
  "name": "scPharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCRM",
  "name": "Screaming Eagle Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCRMU",
  "name": "Screaming Eagle Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCRMW",
  "name": "Screaming Eagle Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCSC",
  "name": "ScanSource, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCVL",
  "name": "Shoe Carnival, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCWO",
  "name": "374Water Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCWX",
  "name": "SecureWorks Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCYX",
  "name": "SCYNEXIS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SCZ",
  "name": "iShares MSCI EAFE Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDA",
  "name": "SunCar Technology Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDAWW",
  "name": "SunCar Technology Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDG",
  "name": "iShares MSCI Global Sustainable Development Goals ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDGR",
  "name": "Schrodinger, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDIG",
  "name": "Stronghold Digital Mining, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDOT",
  "name": "Sadot Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDSI",
  "name": "American Century Short Duration Strategic Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SDVY",
  "name": "First Trust SMID Cap Rising Dividend Achievers ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEAT",
  "name": "Vivid Seats Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEATW",
  "name": "Vivid Seats Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEDG",
  "name": "SolarEdge Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEED",
  "name": "Origin Agritech Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEEL",
  "name": "Seelos Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEER",
  "name": "Seer, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEIC",
  "name": "SEI Investments Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SELF",
  "name": "Global Self Storage, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SELX",
  "name": "Semilux International Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SENEA",
  "name": "Seneca Foods Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SENEB",
  "name": "Seneca Foods Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEPA",
  "name": "SEP Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEPAU",
  "name": "SEP Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEPAW",
  "name": "SEP Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SERA",
  "name": "Sera Prognostics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SERV",
  "name": "Serve Robotics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SETM",
  "name": "Sprott Energy Transition Materials ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEVN",
  "name": "Seven Hills Realty Trust  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SEZL",
  "name": "Sezzle Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFBC",
  "name": "Sound Financial Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFIX",
  "name": "Stitch Fix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFLO",
  "name": "VictoryShares Small Cap Free Cash Flow ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFM",
  "name": "Sprouts Farmers Market, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFNC",
  "name": "Simmons First National Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFST",
  "name": "Southern First Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SFWL",
  "name": "Shengfeng Development Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGA",
  "name": "Saga Communications, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGBX",
  "name": "Safe & Green Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGC",
  "name": "Superior Group of Companies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGD",
  "name": "Safe and Green Development Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGH",
  "name": "SMART Global Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGHT",
  "name": "Sight Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGLY",
  "name": "Singularity Future Technology Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGMA",
  "name": "SigmaTron International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGML",
  "name": "Sigma Lithium Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGMO",
  "name": "Sangamo Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGMT",
  "name": "Sagimet Biosciences Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGRP",
  "name": "SPAR Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SGRY",
  "name": "Surgery Partners, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHBI",
  "name": "Shore Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHC",
  "name": "Sotera Health Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHCR",
  "name": "Sharecare, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHCRW",
  "name": "Sharecare, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHEN",
  "name": "Shenandoah Telecommunications Co ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHFS",
  "name": "SHF Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHFSW",
  "name": "SHF Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHIM",
  "name": "Shimmick Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHIP",
  "name": "Seanergy Maritime Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHLS",
  "name": "Shoals Technologies Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHLT",
  "name": "SHL Telemedicine Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHMD",
  "name": "SCHMID Group N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHMDW",
  "name": "SCHMID Group N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHOO",
  "name": "Steven Madden, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHOT",
  "name": "Safety Shot, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHOTW",
  "name": "Safety Shot, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHPH",
  "name": "Shuttle Pharmaceuticals Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHPW",
  "name": "Shapeways Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHPWW",
  "name": "Shapeways Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHRY",
  "name": "First Trust Bloomberg Shareholder Yield ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHV",
  "name": "iShares Short Treasury Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHY",
  "name": "iShares 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SHYF",
  "name": "The Shyft Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIBN",
  "name": "SI",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIDU",
  "name": "Sidus Space, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIEB",
  "name": "Siebert Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIFY",
  "name": "Sify Technologies Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIGA",
  "name": "SIGA Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIGI",
  "name": "Selective Insurance Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIGIP",
  "name": "Selective Insurance Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SILC",
  "name": "Silicom Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SILK",
  "name": "Silk Road Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SILO",
  "name": "Silo Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIMO",
  "name": "Silicon Motion Technology Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SINT",
  "name": "SiNtx Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SIRI",
  "name": "Sirius XM Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SISI",
  "name": "Shineco, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SITM",
  "name": "SiTime Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SJ",
  "name": "Scienjoy Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKGR",
  "name": "SK Growth Opportunities Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKGRU",
  "name": "SK Growth Opportunities Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKGRW",
  "name": "SK Growth Opportunities Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKIN",
  "name": "The Beauty Health Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKOR",
  "name": "FlexShares Credit",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKRE",
  "name": "Tuttle Capital Daily 2X Inverse Regional Banks ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKWD",
  "name": "Skyward Specialty Insurance Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKYE",
  "name": "Skye Bioscience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKYT",
  "name": "SkyWater Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKYU",
  "name": "ProShares Ultra Cloud Computing",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKYW",
  "name": "SkyWest, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKYX",
  "name": "SKYX Platforms Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SKYY",
  "name": "First Trust Cloud Computing ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLAB",
  "name": "Silicon Laboratories, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLAM",
  "name": "Slam Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLAMU",
  "name": "Slam Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLAMW",
  "name": "Slam Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLDB",
  "name": "Solid Biosciences Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLDP",
  "name": "Solid Power, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLDPW",
  "name": "Solid Power, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLE",
  "name": "Super League Enterprise, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLGL",
  "name": "Sol",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLM",
  "name": "SLM Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLMBP",
  "name": "SLM Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLN",
  "name": "Silence Therapeutics Plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLNA",
  "name": "Selina Hospitality PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLNAW",
  "name": "Selina Hospitality PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLNG",
  "name": "Stabilis Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLNH",
  "name": "Soluna Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLNHP",
  "name": "Soluna Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLNO",
  "name": "Soleno Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLP",
  "name": "Simulations Plus, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLQD",
  "name": "iShares 0",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLRC",
  "name": "SLR Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLRN",
  "name": "ACELYRIN, INC.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLRX",
  "name": "Salarius Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLS",
  "name": "SELLAS Life Sciences Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SLVO",
  "name": "Credit Suisse X",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMBC",
  "name": "Southern Missouri Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMCF",
  "name": "Themes US Small Cap Cash Flow Champions ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMCI",
  "name": "Super Micro Computer, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMCO",
  "name": "Hilton Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMCP",
  "name": "AlphaMark Actively Managed Small Cap ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMFL",
  "name": "Smart for Life, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMH",
  "name": "VanEck Semiconductor ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMID",
  "name": "Smith",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMLR",
  "name": "Semler Scientific, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMMT",
  "name": "Summit Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMPL",
  "name": "The Simply Good Foods Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMRI",
  "name": "Bushido Capital US Equity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMSI",
  "name": "Smith Micro Software, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMTC",
  "name": "Semtech Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMTI",
  "name": "Sanara MedTech Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMX",
  "name": "SMX (Security Matters) Public Limited Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMXT",
  "name": "Solarmax Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SMXWW",
  "name": "SMX (Security Matters) Public Limited Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNAL",
  "name": "Snail, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNAX",
  "name": "Stryve Foods, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNAXW",
  "name": "Stryve Foods, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNBR",
  "name": "Sleep Number Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNCR",
  "name": "Synchronoss Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNCRL",
  "name": "Synchronoss Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNCY",
  "name": "Sun Country Airlines Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SND",
  "name": "Smart Sand, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNDL",
  "name": "SNDL Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNDX",
  "name": "Syndax Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNES",
  "name": "SenesTech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNEX",
  "name": "StoneX Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNFCA",
  "name": "Security National Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNGX",
  "name": "Soligenix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNOA",
  "name": "Sonoma Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNPO",
  "name": "Snap One Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNPS",
  "name": "Synopsys, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNPX",
  "name": "Synaptogenix, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNSE",
  "name": "Sensei Biotherapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNSR",
  "name": "Global X Internet of Things ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNT",
  "name": "Senstar Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNTG",
  "name": "Sentage Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNTI",
  "name": "Senti Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SNY",
  "name": "Sanofi ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOBR",
  "name": "SOBR Safe, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOCL",
  "name": "Global X Social Media ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOFI",
  "name": "SoFi Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOGP",
  "name": "Sound Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOHO",
  "name": "Sotherly Hotels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOHOB",
  "name": "Sotherly Hotels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOHON",
  "name": "Sotherly Hotels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOHOO",
  "name": "Sotherly Hotels Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOHU",
  "name": "Sohu.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOND",
  "name": "Sonder Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SONDW",
  "name": "Sonder Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SONM",
  "name": "Sonim Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SONN",
  "name": "Sonnet BioTherapeutics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SONO",
  "name": "Sonos, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOPA",
  "name": "Society Pass Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOPH",
  "name": "SOPHiA GENETICS SA ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOTK",
  "name": "Sono",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOUN",
  "name": "SoundHound AI, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOUNW",
  "name": "SoundHound AI, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOWG",
  "name": "Sow Good Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOXQ",
  "name": "Invesco PHLX Semiconductor ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SOXX",
  "name": "iShares Semiconductor ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SP",
  "name": "SP Plus Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPAM",
  "name": "Themes Cybersecurity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPAQ",
  "name": "Horizon Kinetics SPAC Active ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPBC",
  "name": "Simplify U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPC",
  "name": "CrossingBridge Pre",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPCB",
  "name": "SuperCom, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPCX",
  "name": "AXS SPAC and New Issue ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPEC",
  "name": "Spectaire Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPECW",
  "name": "Spectaire Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPFI",
  "name": "South Plains Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPGC",
  "name": "Sacks Parente Golf, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPI",
  "name": "SPI Energy Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPKL",
  "name": "Spark I Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPKLU",
  "name": "Spark I Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPKLW",
  "name": "Spark I Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPNS",
  "name": "Sapiens International Corporation N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPOK",
  "name": "Spok Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPPL",
  "name": "SIMPPLE LTD.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPRB",
  "name": "Spruce Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPRC",
  "name": "SciSparc Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPRO",
  "name": "Spero Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPRX",
  "name": "Spear Alpha ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPRY",
  "name": "ARS Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPSC",
  "name": "SPS Commerce, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPT",
  "name": "Sprout Social, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPTN",
  "name": "SpartanNash Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPWH",
  "name": "Sportsman's Warehouse Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SPWR",
  "name": "SunPower Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SQFT",
  "name": "Presidio Property Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SQFTP",
  "name": "Presidio Property Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SQFTW",
  "name": "Presidio Property Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SQLV",
  "name": "Royce Quant Small",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SQQQ",
  "name": "ProShares UltraPro Short QQQ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRAD",
  "name": "Sportradar Group AG ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRBK",
  "name": "SR Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRCE",
  "name": "1st Source Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRCL",
  "name": "Stericycle, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRDX",
  "name": "Surmodics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRET",
  "name": "Global X SuperDividend REIT ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRM",
  "name": "SRM Entertainment, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRPT",
  "name": "Sarepta Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRRK",
  "name": "Scholar Rock Holding Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRTS",
  "name": "Sensus Healthcare, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRZN",
  "name": "Surrozen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SRZNW",
  "name": "Surrozen, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSBI",
  "name": "Summit State Bank ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSBK",
  "name": "Southern States Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSIC",
  "name": "Silver Spike Investment Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSKN",
  "name": "Strata Skin Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSNC",
  "name": "SS&C Technologies Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSNT",
  "name": "SilverSun Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSP",
  "name": "E.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSRM",
  "name": "SSR Mining Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSSS",
  "name": "SuRo Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSSSL",
  "name": "SuRo Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSTI",
  "name": "SoundThinking, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SSYS",
  "name": "Stratasys, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STAA",
  "name": "STAAR Surgical Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STAF",
  "name": "Staffing 360 Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STBA",
  "name": "S&T Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STBX",
  "name": "Starbox Group Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STCN",
  "name": "Steel Connect, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STEP",
  "name": "StepStone Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STER",
  "name": "Sterling Check Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STGW",
  "name": "Stagwell Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STHO",
  "name": "Star Holdings ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STI",
  "name": "Solidion Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STIM",
  "name": "Neuronetics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STKH",
  "name": "Steakholder Foods Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STKL",
  "name": "SunOpta, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STKS",
  "name": "The ONE Group Hospitality, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STLD",
  "name": "Steel Dynamics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STNE",
  "name": "StoneCo Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STOK",
  "name": "Stoke Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRA",
  "name": "Strategic Education, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRL",
  "name": "Sterling Infrastructure, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRM",
  "name": "Streamline Health Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRO",
  "name": "Sutro Biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRR",
  "name": "Star Equity Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRRP",
  "name": "Star Equity Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRS",
  "name": "Stratus Properties Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STRT",
  "name": "STRATTEC SECURITY CORPORATION ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STSS",
  "name": "Sharps Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STSSW",
  "name": "Sharps Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STTK",
  "name": "Shattuck Labs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "STX",
  "name": "Seagate Technology Holdings PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SUGP",
  "name": "SU Group Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SUPN",
  "name": "Supernus Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SURG",
  "name": "SurgePays, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SURGW",
  "name": "SurgePays, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SUSB",
  "name": "iShares ESG Aware 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SUSC",
  "name": "iShares ESG Aware USD Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SUSL",
  "name": "iShares ESG MSCI USA Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SUUN",
  "name": "SolarBank Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVA",
  "name": "Sinovac Biotech, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVC",
  "name": "Service Properties Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVII",
  "name": "Spring Valley Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVIIR",
  "name": "Spring Valley Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVIIU",
  "name": "Spring Valley Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVIIW",
  "name": "Spring Valley Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVMH",
  "name": "SRIVARU Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVMHW",
  "name": "SRIVARU Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVRA",
  "name": "Savara, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVRE",
  "name": "SaverOne 2014 Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SVREW",
  "name": "SaverOne 2014 Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWAG",
  "name": "Stran & Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWAGW",
  "name": "Stran & Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWAV",
  "name": "Shockwave Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWBI",
  "name": "Smith & Wesson Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWIM",
  "name": "Latham Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWIN",
  "name": "Solowin Holdings ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWKH",
  "name": "SWK Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWKHL",
  "name": "SWK Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWKS",
  "name": "Skyworks Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWSS",
  "name": "Clean Energy Special Situations Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWSSU",
  "name": "Clean Energy Special Situations Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWSSW",
  "name": "Clean Energy Special Situations Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWTX",
  "name": "SpringWorks Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWVL",
  "name": "Swvl Holdings Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SWVLW",
  "name": "Swvl Holdings Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SXTC",
  "name": "China SXT Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SXTP",
  "name": "60 Degrees Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SXTPW",
  "name": "60 Degrees Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SY",
  "name": "So",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYBT",
  "name": "Stock Yards Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYBX",
  "name": "Synlogic, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYM",
  "name": "Symbotic Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYNA",
  "name": "Synaptics Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYPR",
  "name": "Sypris Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYRA",
  "name": "Syra Health Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYRE",
  "name": "Spyre Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYRS",
  "name": "Syros Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYT",
  "name": "SYLA Technologies Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYTA",
  "name": "Siyata Mobile, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "SYTAW",
  "name": "Siyata Mobile, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TACT",
  "name": "TransAct Technologies Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TAIT",
  "name": "Taitron Components Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TALK",
  "name": "Talkspace, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TALKW",
  "name": "Talkspace, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TANH",
  "name": "Tantech Holdings Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TAOP",
  "name": "Taoping Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TARA",
  "name": "Protara Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TARK",
  "name": "AXS 2X Innovation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TARS",
  "name": "Tarsus Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TASK",
  "name": "TaskUs, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TAST",
  "name": "Carrols Restaurant Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TATT",
  "name": "TAT Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TAYD",
  "name": "Taylor Devices, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBBK",
  "name": "The Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBIL",
  "name": "US Treasury 3 Month Bill ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBIO",
  "name": "Telesis Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBLA",
  "name": "Taboola.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBLAW",
  "name": "Taboola.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBLD",
  "name": "Thornburg Income Builder Opportunities Trust ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBLT",
  "name": "ToughBuilt Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBMC",
  "name": "Trailblazer Merger Corporation I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBMCR",
  "name": "Trailblazer Merger Corporation I ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBNK",
  "name": "Territorial Bancorp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBPH",
  "name": "Theravance Biopharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TBRG",
  "name": "TruBridge, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TC",
  "name": "TuanChe Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBC",
  "name": "TC Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBI",
  "name": "Texas Capital Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBIO",
  "name": "Texas Capital Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBK",
  "name": "TriCo Bancshares ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBP",
  "name": "TC BioPharm (Holdings) plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBPW",
  "name": "TC BioPharm (Holdings) plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBS",
  "name": "Texas Community Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCBX",
  "name": "Third Coast Bancshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCHI",
  "name": "iShares MSCI China Multisector Tech ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCJH",
  "name": "Top KingWin Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCMD",
  "name": "Tactile Systems Technology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCOM",
  "name": "Trip.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCON",
  "name": "TRACON Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCPC",
  "name": "BlackRock TCP Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCRT",
  "name": "Alaunos Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCRX",
  "name": "TScan Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCTM",
  "name": "TCTM Kids IT Education Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TCX",
  "name": "Tucows Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TDI",
  "name": "Touchstone Dynamic International ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TDIV",
  "name": "First Trust NASDAQ Technology Dividend Index Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TDSB",
  "name": "Cabana Target Beta ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TDSC",
  "name": "Cabana Target Drawdown 10 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TDUP",
  "name": "ThredUp Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TEAM",
  "name": "Atlassian Corporation  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TECH",
  "name": "Bio",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TECTP",
  "name": "Tectonic Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TELA",
  "name": "TELA Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TELO",
  "name": "Telomir Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TENB",
  "name": "Tenable Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TENK",
  "name": "TenX Keane Acquisition ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TENKR",
  "name": "TenX Keane Acquisition ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TENKU",
  "name": "TenX Keane Acquisition ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TENX",
  "name": "Tenax Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TER",
  "name": "Teradyne, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TERN",
  "name": "Terns Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TETE",
  "name": "Technology & Telecommunication Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TETEU",
  "name": "Technology & Telecommunication Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TETEW",
  "name": "Technology & Telecommunication Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TFFP",
  "name": "TFF Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TFIN",
  "name": "Triumph Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TFINP",
  "name": "Triumph Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TFSL",
  "name": "TFS Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TGAA",
  "name": "Target Global Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TGAAU",
  "name": "Target Global Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TGAAW",
  "name": "Target Global Acquisition I Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TGAN",
  "name": "Transphorm, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TGL",
  "name": "Treasure Global Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TGTX",
  "name": "TG Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TH",
  "name": "Target Hospitality Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THAR",
  "name": "Tharimmune, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THCH",
  "name": "TH International Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THCP",
  "name": "Thunder Bridge Capital Partners IV, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THCPU",
  "name": "Thunder Bridge Capital Partners IV, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THCPW",
  "name": "Thunder Bridge Capital Partners IV, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THFF",
  "name": "First Financial Corporation Indiana ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THMO",
  "name": "ThermoGenesis Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THRD",
  "name": "Third Harmonic Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THRM",
  "name": "Gentherm Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THRY",
  "name": "Thryv Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "THTX",
  "name": "Theratechnologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TIGO",
  "name": "Millicom International Cellular S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TIGR",
  "name": "UP Fintech Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TIL",
  "name": "Instil Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TILE",
  "name": "Interface, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TIPT",
  "name": "Tiptree Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TIRX",
  "name": "TIAN RUIXIANG Holdings Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TITN",
  "name": "Titan Machinery Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TIVC",
  "name": "Tivic Health Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TKLF",
  "name": "Yoshitsu Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TKNO",
  "name": "Alpha Teknova, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLF",
  "name": "Tandy Leather Factory, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLGY",
  "name": "TLGY Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLGYU",
  "name": "TLGY Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLGYW",
  "name": "TLGY Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLIS",
  "name": "Talis Biomedical Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLPH",
  "name": "Talphera, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLRY",
  "name": "Tilray Brands, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLS",
  "name": "Telos Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLSA",
  "name": "Tiziana Life Sciences Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLSI",
  "name": "TriSalus Life Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLSIW",
  "name": "TriSalus Life Sciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TLT",
  "name": "iShares 20+ Year Treasury Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMC",
  "name": "TMC the metals company Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMCI",
  "name": "Treace Medical Concepts, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMCWW",
  "name": "TMC the metals company Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMDX",
  "name": "TransMedics Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMET",
  "name": "iShares Transition",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMTC",
  "name": "TMT Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMTCR",
  "name": "TMT Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMTCU",
  "name": "TMT Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TMUS",
  "name": "T",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TNDM",
  "name": "Tandem Diabetes Care, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TNGX",
  "name": "Tango Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TNON",
  "name": "Tenon Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TNONW",
  "name": "Tenon Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TNXP",
  "name": "Tonix Pharmaceuticals Holding Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TNYA",
  "name": "Tenaya Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TOI",
  "name": "The Oncology Institute, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TOIIW",
  "name": "The Oncology Institute, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TOMZ",
  "name": "TOMI Environmental Solutions, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TOP",
  "name": "TOP Financial Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TORO",
  "name": "Toro Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TOUR",
  "name": "Tuniu Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TOWN",
  "name": "Towne Bank ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TPCS",
  "name": "TechPrecision Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TPG",
  "name": "TPG Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TPGXL",
  "name": "TPG Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TPIC",
  "name": "TPI Composites, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TPST",
  "name": "Tempest Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TQQQ",
  "name": "ProShares UltraPro QQQ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRAW",
  "name": "Traws Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRDA",
  "name": "Entrada Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TREE",
  "name": "LendingTree, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRES",
  "name": "Defiance Treasury Alternative Yield ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRIB",
  "name": "Trinity Biotech plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRIN",
  "name": "Trinity Capital Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRINL",
  "name": "Trinity Capital Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRINZ",
  "name": "Trinity Capital Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRIP",
  "name": "TripAdvisor, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRMB",
  "name": "Trimble Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRMD",
  "name": "TORM plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRMK",
  "name": "Trustmark Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRML",
  "name": "Tourmaline Bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRNR",
  "name": "Interactive Strength Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRNS",
  "name": "Transcat, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRON",
  "name": "Corner Growth Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRONU",
  "name": "Corner Growth Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRONW",
  "name": "Corner Growth Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TROO",
  "name": "TROOPS, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TROW",
  "name": "T.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRS",
  "name": "TriMas Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRSG",
  "name": "Tungray Technologies Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRST",
  "name": "TrustCo Bank Corp NY ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRUE",
  "name": "TrueCar, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRUG",
  "name": "TruGolf Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRUP",
  "name": "Trupanion, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRVG",
  "name": "trivago N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRVI",
  "name": "Trevi Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TRVN",
  "name": "Trevena, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSAT",
  "name": "Telesat Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSBK",
  "name": "Timberland Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSBX",
  "name": "Turnstone Biologics Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSCO",
  "name": "Tractor Supply Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSDD",
  "name": "GraniteShares 2x Short TSLA Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSEM",
  "name": "Tower Semiconductor Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSHA",
  "name": "Taysha Gene Therapies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSL",
  "name": "GraniteShares 1.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLA",
  "name": "Tesla, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLL",
  "name": "Direxion Daily TSLA Bull 2X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLQ",
  "name": "AXS TSLA Bear Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLR",
  "name": "GraniteShares 2x Long TSLA Daily ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLS",
  "name": "Direxion Daily TSLA Bear 1X Shares",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLT",
  "name": "T",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSLZ",
  "name": "T",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSRI",
  "name": "TSR, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TSVT",
  "name": "2seventy bio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTD",
  "name": "The Trade Desk, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTEC",
  "name": "TTEC Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTEK",
  "name": "Tetra Tech, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTGT",
  "name": "TechTarget, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTMI",
  "name": "TTM Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTNP",
  "name": "Titan Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTOO",
  "name": "T2 Biosystems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTSH",
  "name": "Tile Shop Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TTWO",
  "name": "Take",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TUG",
  "name": "STF Tactical Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TUGN",
  "name": "STF Tactical Growth & Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TUR",
  "name": "iShares MSCI Turkey ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TURB",
  "name": "Turbo Energy, S.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TURN",
  "name": "180 Degree Capital Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TUSK",
  "name": "Mammoth Energy Services, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TVGN",
  "name": "Tevogen Bio Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TVGNW",
  "name": "Tevogen Bio Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TVTX",
  "name": "Travere Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TW",
  "name": "Tradeweb Markets Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWG",
  "name": "Top Wealth Group Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWIN",
  "name": "Twin Disc, Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWKS",
  "name": "Thoughtworks Holding, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWLV",
  "name": "Twelve Seas Investment Company II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWLVU",
  "name": "Twelve Seas Investment Company II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWLVW",
  "name": "Twelve Seas Investment Company II ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWOU",
  "name": "2U, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TWST",
  "name": "Twist Bioscience Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TXG",
  "name": "10x Genomics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TXMD",
  "name": "TherapeuticsMD, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TXN",
  "name": "Texas Instruments Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TXRH",
  "name": "Texas Roadhouse, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TXSS",
  "name": "Texas Capital Texas Small Cap Equity Index ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TYGO",
  "name": "Tigo Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TYRA",
  "name": "Tyra Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "TZOO",
  "name": "Travelzoo ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UAE",
  "name": "iShares MSCI UAE ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UAL",
  "name": "United Airlines Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UBCP",
  "name": "United Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UBFO",
  "name": "United Security Bancshares ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UBND",
  "name": "VictoryShares Core Plus Intermediate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UBSI",
  "name": "United Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UBX",
  "name": "Unity Biotechnology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UBXG",
  "name": "U",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCAR",
  "name": "U Power Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCBI",
  "name": "United Community Banks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCBIO",
  "name": "United Community Banks, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCL",
  "name": "uCloudlink Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCRD",
  "name": "VictoryShares Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCTT",
  "name": "Ultra Clean Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UCYB",
  "name": "ProShares Ultra Nasdaq Cybersecurity",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UDMY",
  "name": "Udemy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UEIC",
  "name": "Universal Electronics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UEVM",
  "name": "VictoryShares Emerging Markets Value Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UFCS",
  "name": "United Fire Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UFIV",
  "name": "US Treasury 5 Year Note ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UFO",
  "name": "Procure Space ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UFPI",
  "name": "UFP Industries, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UFPT",
  "name": "UFP Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UG",
  "name": "United",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UGRO",
  "name": "urban",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UHG",
  "name": "United Homes Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UHGWW",
  "name": "United Homes Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UITB",
  "name": "VictoryShares Core Intermediate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UIVM",
  "name": "VictoryShares International Value Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UK",
  "name": "Ucommune International Ltd  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UKOMW",
  "name": "Ucommune International Ltd  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ULBI",
  "name": "Ultralife Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ULCC",
  "name": "Frontier Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ULH",
  "name": "Universal Logistics Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ULTA",
  "name": "Ulta Beauty, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ULVM",
  "name": "VictoryShares US Value Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ULY",
  "name": "Urgent.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UMBF",
  "name": "UMB Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UMMA",
  "name": "Wahed Dow Jones Islamic World ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UNB",
  "name": "Union Bankshares, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UNCY",
  "name": "Unicycive Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UNIT",
  "name": "Uniti Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UNIY",
  "name": "WisdomTree Voya Yield Enhanced USD Universal Bond Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UNTY",
  "name": "Unity Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UONE",
  "name": "Urban One, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UONEK",
  "name": "Urban One, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPBD",
  "name": "Upbound Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPC",
  "name": "Universe Pharmaceuticals Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPGR",
  "name": "Xtrackers US Green Infrastructure Select Equity ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPLD",
  "name": "Upland Software, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPST",
  "name": "Upstart Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPWK",
  "name": "Upwork Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UPXI",
  "name": "Upexi, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "URBN",
  "name": "Urban Outfitters, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "URGN",
  "name": "UroGen Pharma Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "URNJ",
  "name": "Sprott Junior Uranium Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UROY",
  "name": "Uranium Royalty Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USAP",
  "name": "Universal Stainless & Alloy Products, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USAU",
  "name": "U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USBF",
  "name": "iShares USD Systematic Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USCB",
  "name": "USCB Financial Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USCF",
  "name": "Themes US Cash Flow Champions ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USCL",
  "name": "iShares Climate Conscious & Transition MSCI USA ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USDX",
  "name": "SGI Enhanced Core ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USEA",
  "name": "United Maritime Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USEG",
  "name": "U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USFI",
  "name": "BrandywineGLOBAL ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USGO",
  "name": "U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USGOW",
  "name": "U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USIG",
  "name": "iShares Broad USD Investment Grade Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USIN",
  "name": "WisdomTree 7",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USIO",
  "name": "Usio, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USLM",
  "name": "United States Lime & Minerals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USMC",
  "name": "Principal U.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USOI",
  "name": "Credit Suisse X",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USRD",
  "name": "Themes US R&D Champions ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USSH",
  "name": "WisdomTree 1",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USTB",
  "name": "VictoryShares Short",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USVM",
  "name": "VictoryShares US Small Mid Cap Value Momentum ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USVN",
  "name": "US Treasury 7 Year Note ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "USXF",
  "name": "iShares ESG Advanced MSCI USA ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTEN",
  "name": "US Treasury 10 Year Note ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTHR",
  "name": "United Therapeutics Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTHY",
  "name": "US Treasury 30 Year Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTMD",
  "name": "Utah Medical Products, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTRE",
  "name": "US Treasury 3 Year Note ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTSI",
  "name": "UTStarcom Holdings Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTWO",
  "name": "US Treasury 2 Year Note ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UTWY",
  "name": "US Treasury 20 Year Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UVSP",
  "name": "Univest Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "UXIN",
  "name": "Uxin Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VABK",
  "name": "Virginia National Bankshares Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VALN",
  "name": "Valneva SE ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VALU",
  "name": "Value Line, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VANI",
  "name": "Vivani Medical, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VBFC",
  "name": "Village Bank and Trust Financial Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VBIV",
  "name": "VBI Vaccines, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VBNK",
  "name": "VersaBank ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VBTX",
  "name": "Veritex Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VC",
  "name": "Visteon Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCEL",
  "name": "Vericel Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCIG",
  "name": "VCI Global Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCIT",
  "name": "Vanguard Intermediate",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCLT",
  "name": "Vanguard Long",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCNX",
  "name": "Vaccinex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCRB",
  "name": "Vanguard Core Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCSA",
  "name": "Vacasa, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCSH",
  "name": "Vanguard Short",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCTR",
  "name": "Victory Capital Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VCYT",
  "name": "Veracyte, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VECO",
  "name": "Veeco Instruments Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VEEE",
  "name": "Twin Vee PowerCats Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VEON",
  "name": "VEON Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERA",
  "name": "Vera Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERB",
  "name": "Verb Technology Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERI",
  "name": "Veritone, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERO",
  "name": "Venus Concept Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERU",
  "name": "Veru Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERV",
  "name": "Verve Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERX",
  "name": "Vertex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VERY",
  "name": "Vericity, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VEV",
  "name": "Vicinity Motor Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VFF",
  "name": "Village Farms International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VFLO",
  "name": "VictoryShares Free Cash Flow ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VFS",
  "name": "VinFast Auto Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VFSWW",
  "name": "VinFast Auto Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VGAS",
  "name": "Verde Clean Fuels, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VGASW",
  "name": "Verde Clean Fuels, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VGIT",
  "name": "Vanguard Intermediate",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VGLT",
  "name": "Vanguard Long",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VGSH",
  "name": "Vanguard Short",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VGSR",
  "name": "Vert Global Sustainable Real Estate ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIA",
  "name": "Via Renewables, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIASP",
  "name": "Via Renewables, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIAV",
  "name": "Viavi Solutions Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VICR",
  "name": "Vicor Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIGI",
  "name": "Vanguard International Dividend Appreciation ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIGL",
  "name": "Vigil Neuroscience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VINC",
  "name": "Vincerx Pharma, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VINO",
  "name": "Gaucho Group Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VINP",
  "name": "Vinci Partners Investments Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIOT",
  "name": "Viomi Technology Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIR",
  "name": "Vir Biotechnology, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIRC",
  "name": "Virco Manufacturing Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIRI",
  "name": "Virios Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIRT",
  "name": "Virtu Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIRX",
  "name": "Viracta Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VISL",
  "name": "Vislink Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VITL",
  "name": "Vital Farms, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VIVK",
  "name": "Vivakor, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VKTX",
  "name": "Viking Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VLCN",
  "name": "Volcon, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VLGEA",
  "name": "Village Super Market, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VLY",
  "name": "Valley National Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VLYPO",
  "name": "Valley National Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VLYPP",
  "name": "Valley National Bancorp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMAR",
  "name": "Vision Marine Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMBS",
  "name": "Vanguard Mortgage",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMCA",
  "name": "Valuence Merger Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMCAU",
  "name": "Valuence Merger Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMCAW",
  "name": "Valuence Merger Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMD",
  "name": "Viemed Healthcare, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMEO",
  "name": "Vimeo, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VMOT",
  "name": "Alpha Architect Value Momentum Trend ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VNDA",
  "name": "Vanda Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VNET",
  "name": "VNET Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VNOM",
  "name": "Viper Energy, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VNQI",
  "name": "Vanguard Global ex",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VOD",
  "name": "Vodafone Group Plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VONE",
  "name": "Vanguard Russell 1000 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VONG",
  "name": "Vanguard Russell 1000 Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VONV",
  "name": "Vanguard Russell 1000 Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VOR",
  "name": "Vor Biopharma Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VOXR",
  "name": "Vox Royalty Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VOXX",
  "name": "VOXX International Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VPLS",
  "name": "Vanguard Core Plus Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRA",
  "name": "Vera Bradley, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRAR",
  "name": "The Glimpse Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRAX",
  "name": "Virax Biolabs Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRCA",
  "name": "Verrica Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRDN",
  "name": "Viridian Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VREX",
  "name": "Varex Imaging Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRIG",
  "name": "Invesco Variable Rate Investment Grade ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRM",
  "name": "Vroom, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRME",
  "name": "VerifyMe, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRMEW",
  "name": "VerifyMe, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRNA",
  "name": "Verona Pharma plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRNS",
  "name": "Varonis Systems, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRNT",
  "name": "Verint Systems Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRPX",
  "name": "Virpax Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRRM",
  "name": "Verra Mobility Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRSK",
  "name": "Verisk Analytics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRSN",
  "name": "VeriSign, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VRTX",
  "name": "Vertex Pharmaceuticals Incorporated ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VS",
  "name": "Versus Systems Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSAC",
  "name": "Vision Sensing Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSACU",
  "name": "Vision Sensing Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSACW",
  "name": "Vision Sensing Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSAT",
  "name": "ViaSat, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSDA",
  "name": "VictoryShares Dividend Accelerator ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSEC",
  "name": "VSE Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSME",
  "name": "VS Media Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSMV",
  "name": "VictoryShares US Multi",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSSYW",
  "name": "Versus Systems Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSTA",
  "name": "Vasta Platform Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSTE",
  "name": "Vast Renewables Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSTEW",
  "name": "Vast Renewables Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VSTM",
  "name": "Verastem, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTC",
  "name": "Vanguard Total Corporate Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTGN",
  "name": "Vistagen Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTHR",
  "name": "Vanguard Russell 3000 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTIP",
  "name": "Vanguard Short",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTNR",
  "name": "Vertex Energy, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTRS",
  "name": "Viatris Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTRU",
  "name": "Vitru Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTSI",
  "name": "VirTra, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTVT",
  "name": "vTv Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTWG",
  "name": "Vanguard Russell 2000 Growth ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTWO",
  "name": "Vanguard Russell 2000 ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTWV",
  "name": "Vanguard Russell 2000 Value ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VTYX",
  "name": "Ventyx Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VUZI",
  "name": "Vuzix Corporation  ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VVOS",
  "name": "Vivos Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VVPR",
  "name": "VivoPower International PLC ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VWE",
  "name": "Vintage Wine Estates, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VWEWW",
  "name": "Vintage Wine Estates, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VWOB",
  "name": "Vanguard Emerging Markets Government Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VXRT",
  "name": "Vaxart, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VXUS",
  "name": "Vanguard Total International Stock ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VYGR",
  "name": "Voyager Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VYMI",
  "name": "Vanguard International High Dividend Yield ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "VYNE",
  "name": "VYNE Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WABC",
  "name": "Westamerica Bancorporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WABF",
  "name": "Western Asset Bond ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAFD",
  "name": "WaFd, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAFDP",
  "name": "WaFd, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAFU",
  "name": "Wah Fu Education Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WALD",
  "name": "Waldencast plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WALDW",
  "name": "Waldencast plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WASH",
  "name": "Washington Trust Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WATT",
  "name": "Energous Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAVD",
  "name": "WaveDancer, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAVE",
  "name": "Eco Wave Power Global AB (publ) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAVS",
  "name": "Western Acquisition Ventures Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAVSU",
  "name": "Western Acquisition Ventures Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WAVSW",
  "name": "Western Acquisition Ventures Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WB",
  "name": "Weibo Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WBA",
  "name": "Walgreens Boots Alliance, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WBD",
  "name": "Warner Bros.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WBND",
  "name": "Western Asset Total Return ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WBUY",
  "name": "WEBUY GLOBAL LTD.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WCBR",
  "name": "WisdomTree Cybersecurity Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WCLD",
  "name": "WisdomTree Cloud Computing Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WDAY",
  "name": "Workday, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WDC",
  "name": "Western Digital Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WDFC",
  "name": "WD",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WEEI",
  "name": "Westwood Salient Enhanced Energy Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WEN",
  "name": "Wendy's Company (The) ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WERN",
  "name": "Werner Enterprises, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WEST",
  "name": "Westrock Coffee Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WESTW",
  "name": "Westrock Coffee Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WETH",
  "name": "Wetouch Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WEYS",
  "name": "Weyco Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WFCF",
  "name": "Where Food Comes From, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WFRD",
  "name": "Weatherford International plc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WGMI",
  "name": "Valkyrie Bitcoin Miners ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WGS",
  "name": "GeneDx Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WGSWW",
  "name": "GeneDx Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHF",
  "name": "WhiteHorse Finance, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHFCL",
  "name": "WhiteHorse Finance, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHLM",
  "name": "Wilhelmina International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHLR",
  "name": "Wheeler Real Estate Investment Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHLRD",
  "name": "Wheeler Real Estate Investment Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHLRL",
  "name": "Wheeler Real Estate Investment Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WHLRP",
  "name": "Wheeler Real Estate Investment Trust, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WILC",
  "name": "G.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WIMI",
  "name": "WiMi Hologram Cloud Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINA",
  "name": "Winmark Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINC",
  "name": "Western Asset Short Duration Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WING",
  "name": "Wingstop Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINT",
  "name": "Windtree Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINV",
  "name": "WinVest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINVR",
  "name": "WinVest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINVU",
  "name": "WinVest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WINVW",
  "name": "WinVest Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WIRE",
  "name": "Encore Wire Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WISA",
  "name": "WiSA Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WISE",
  "name": "Themes Generative Artificial Intelligence ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WISH",
  "name": "ContextLogic Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WIX",
  "name": "Wix.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WKEY",
  "name": "WISeKey International Holding Ltd ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WKHS",
  "name": "Workhorse Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WKME",
  "name": "WalkMe Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WKSP",
  "name": "Worksport, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WKSPW",
  "name": "Worksport, Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WLDN",
  "name": "Willdan Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WLDS",
  "name": "Wearable Devices Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WLDSW",
  "name": "Wearable Devices Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WLFC",
  "name": "Willis Lease Finance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WLGS",
  "name": "Wang & Lee Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WMG",
  "name": "Warner Music Group Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WMPN",
  "name": "William Penn Bancorporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WNDY",
  "name": "Global X Wind Energy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WNEB",
  "name": "Western New England Bancorp, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WNW",
  "name": "Meiwu Technology Company Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WOOD",
  "name": "iShares Global Timber & Forestry ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WOOF",
  "name": "Petco Health and Wellness Company, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WORX",
  "name": "SCWorx Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WPRT",
  "name": "Westport Fuel Systems Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WRAP",
  "name": "Wrap Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WRLD",
  "name": "World Acceptance Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WRND",
  "name": "IQ Global Equity R&D Leaders ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WRNT",
  "name": "Warrantee Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WSBC",
  "name": "WesBanco, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WSBCP",
  "name": "WesBanco, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WSBF",
  "name": "Waterstone Financial, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WSC",
  "name": "WillScot Mobile Mini Holdings Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WSFS",
  "name": "WSFS Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTBA",
  "name": "West Bancorporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTBN",
  "name": "WisdomTree Bianco Total Return Fund",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTFC",
  "name": "Wintrust Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTFCM",
  "name": "Wintrust Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTFCP",
  "name": "Wintrust Financial Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTMA",
  "name": "Welsbach Technology Metals Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTMAR",
  "name": "Welsbach Technology Metals Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTMAU",
  "name": "Welsbach Technology Metals Acquisition Corp.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTO",
  "name": "UTime Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WTW",
  "name": "Willis Towers Watson Public Limited Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WULF",
  "name": "TeraWulf Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WVE",
  "name": "Wave Life Sciences Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WVVI",
  "name": "Willamette Valley Vineyards, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WVVIP",
  "name": "Willamette Valley Vineyards, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WW",
  "name": "WW International, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WWD",
  "name": "Woodward, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "WYNN",
  "name": "Wynn Resorts, Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XAIR",
  "name": "Beyond Air, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XBIL",
  "name": "US Treasury 6 Month Bill ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XBIO",
  "name": "Xenetic Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XBIOW",
  "name": "Xenetic Biosciences, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XBIT",
  "name": "XBiotech Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XBP",
  "name": "XBP Europe Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XBPEW",
  "name": "XBP Europe Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XCUR",
  "name": "Exicure, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XEL",
  "name": "Xcel Energy Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XELA",
  "name": "Exela Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XELAP",
  "name": "Exela Technologies, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XELB",
  "name": "Xcel Brands, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XENE",
  "name": "Xenon Pharmaceuticals Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XERS",
  "name": "Xeris Biopharma Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XFIN",
  "name": "ExcelFin Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XFINU",
  "name": "ExcelFin Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XFINW",
  "name": "ExcelFin Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XFIX",
  "name": "F\/m Opportunistic Income ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XFOR",
  "name": "X4 Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XGN",
  "name": "Exagen Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XLO",
  "name": "Xilio Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XMTR",
  "name": "Xometry, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XNCR",
  "name": "Xencor, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XNET",
  "name": "Xunlei Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XOMA",
  "name": "XOMA Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XOMAO",
  "name": "XOMA Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XOMAP",
  "name": "XOMA Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XOS",
  "name": "Xos, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XOSWW",
  "name": "Xos, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XP",
  "name": "XP Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XPEL",
  "name": "XPEL, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XPON",
  "name": "Expion360 Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XRAY",
  "name": "DENTSPLY SIRONA Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XRTX",
  "name": "XORTX Therapeutics Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XRX",
  "name": "Xerox Holdings Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XT",
  "name": "iShares Exponential Technologies ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XTIA",
  "name": "XTI Aerospace, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XTKG",
  "name": "X3 Holdings Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XTLB",
  "name": "XTL Biopharmaceuticals Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XWEL",
  "name": "XWELL, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XXII",
  "name": "22nd Century Group, Inc ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "XYLO",
  "name": "Xylo Technologies Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YGMZ",
  "name": "MingZhu Logistics Holdings Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YHGJ",
  "name": "Yunhong Green CTI Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YI",
  "name": "111, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YIBO",
  "name": "Planet Image International Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YJ",
  "name": "Yunji Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YLDE",
  "name": "ClearBridge Dividend Strategy ESG ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YMAB",
  "name": "Y",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YNDX",
  "name": "Yandex N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YORW",
  "name": "The York Water Company ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YOSH",
  "name": "Yoshiharu Global Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YOTA",
  "name": "Yotta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YOTAR",
  "name": "Yotta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YOTAU",
  "name": "Yotta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YOTAW",
  "name": "Yotta Acquisition Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YQ",
  "name": "17 Education & Technology Group Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YS",
  "name": "YS Biopharma Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YSBPW",
  "name": "YS Biopharma Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YTEN",
  "name": "Yield10 Bioscience, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YTRA",
  "name": "Yatra Online, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YY",
  "name": "JOYY Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YYAI",
  "name": "Connexa Sports Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "YYGH",
  "name": "YY Group Holding Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "Z",
  "name": "Zillow Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZAPP",
  "name": "Zapp Electric Vehicles Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZAPPW",
  "name": "Zapp Electric Vehicles Group Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZAZZT",
  "name": "Tick Pilot Test Stock Class A Common Stock",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZBAO",
  "name": "Zhibao Technology Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZBRA",
  "name": "Zebra Technologies Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZBZZT",
  "name": "Test Pilot Test Stock Class B Common Stock",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZCAR",
  "name": "Zoomcar Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZCARW",
  "name": "Zoomcar Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZCMD",
  "name": "Zhongchao Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZCZZT",
  "name": "Tick Pilot Test Stock Class C ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZD",
  "name": "Ziff Davis, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZENV",
  "name": "Zenvia Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZEO",
  "name": "Zeo Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZEOWW",
  "name": "Zeo Energy Corporation ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZEUS",
  "name": "Olympic Steel, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZFOX",
  "name": "ZeroFox Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZFOXW",
  "name": "ZeroFox Holdings, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZG",
  "name": "Zillow Group, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZI",
  "name": "ZoomInfo Technologies Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZIMV",
  "name": "ZimVie Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZION",
  "name": "Zions Bancorporation N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZIONL",
  "name": "Zions Bancorporation N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZIONO",
  "name": "Zions Bancorporation N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZIONP",
  "name": "Zions Bancorporation N.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZJYL",
  "name": "JIN MEDICAL INTERNATIONAL LTD.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZJZZT",
  "name": "NASDAQ TEST STOCK",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZKIN",
  "name": "ZK International Group Co.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZLAB",
  "name": "Zai Lab Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZLS",
  "name": "Zalatoris II Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZLSWU",
  "name": "Zalatoris II Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZLSWW",
  "name": "Zalatoris II Acquisition Corp ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZM",
  "name": "Zoom Video Communications, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZNTL",
  "name": "Zentalis Pharmaceuticals, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZOOZ",
  "name": "ZOOZ Power Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZOOZW",
  "name": "ZOOZ Power Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZPTA",
  "name": "Zapata Computing Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZPTAW",
  "name": "Zapata Computing Holdings Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZS",
  "name": "Zscaler, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZTEK",
  "name": "Zentek Ltd.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZUMZ",
  "name": "Zumiez Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZURA",
  "name": "Zura Bio Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZURAW",
  "name": "Zura Bio Limited ",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZVRA",
  "name": "Zevra Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZVSA",
  "name": "ZyVersa Therapeutics, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZVZZT",
  "name": "NASDAQ TEST STOCK",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZWZZT",
  "name": "NASDAQ TEST STOCK",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZXYZ.A",
  "name": "Nasdaq Symbology Test Common Stock",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZXZZT",
  "name": "NASDAQ TEST STOCK",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZYME",
  "name": "Zymeworks Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZYXI",
  "name": "Zynex, Inc.",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
 {
  "symbol": "ZZZ",
  "name": "Cyber Hornet S&P 500 and Bitcoin 75\/25 Strategy ETF",
  "currency": "USD",
  "stockExchange": "NasdaqGM",
  "exchangeShortName": "NASDAQ"
 },
	{
  "symbol": "095570.KS",
  "name": "AJ네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006840.KS",
  "name": "AK홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "027410.KS",
  "name": "BGF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "282330.KS",
  "name": "BGF리테일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "138930.KS",
  "name": "BNK금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001460.KS",
  "name": "BYC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001465.KS",
  "name": "BYC우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001040.KS",
  "name": "CJ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079160.KS",
  "name": "CJ CGV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00104K.KS",
  "name": "CJ4우(전환)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000120.KS",
  "name": "CJ대한통운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011150.KS",
  "name": "CJ씨푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011155.KS",
  "name": "CJ씨푸드1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001045.KS",
  "name": "CJ우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097950.KS",
  "name": "CJ제일제당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097955.KS",
  "name": "CJ제일제당 우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000480.KS",
  "name": "CR홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000590.KS",
  "name": "CS홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012030.KS",
  "name": "DB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016610.KS",
  "name": "DB금융투자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005830.KS",
  "name": "DB손해보험",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000990.KS",
  "name": "DB하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "139130.KS",
  "name": "DGB금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001530.KS",
  "name": "DI동일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000210.KS",
  "name": "DL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000215.KS",
  "name": "DL우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "375500.KS",
  "name": "DL이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "37550L.KS",
  "name": "DL이앤씨2우(전환)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "37550K.KS",
  "name": "DL이앤씨우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007340.KS",
  "name": "DN오토모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004840.KS",
  "name": "DRB동일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "155660.KS",
  "name": "DSR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069730.KS",
  "name": "DSR제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017860.KS",
  "name": "DS단석",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017940.KS",
  "name": "E1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "365550.KS",
  "name": "ESR켄달스퀘어리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "383220.KS",
  "name": "F&F",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007700.KS",
  "name": "F&F홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "114090.KS",
  "name": "GKL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078930.KS",
  "name": "GS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006360.KS",
  "name": "GS건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001250.KS",
  "name": "GS글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007070.KS",
  "name": "GS리테일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078935.KS",
  "name": "GS우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012630.KS",
  "name": "HDC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "039570.KS",
  "name": "HDC랩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "089470.KS",
  "name": "HDC현대EP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "294870.KS",
  "name": "HDC현대산업개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009540.KS",
  "name": "HD한국조선해양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267250.KS",
  "name": "HD현대",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267270.KS",
  "name": "HD현대건설기계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010620.KS",
  "name": "HD현대미포",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "322000.KS",
  "name": "HD현대에너지솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "042670.KS",
  "name": "HD현대인프라코어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267260.KS",
  "name": "HD현대일렉트릭",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "329180.KS",
  "name": "HD현대중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097230.KS",
  "name": "HJ중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014790.KS",
  "name": "HL D&I",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003580.KS",
  "name": "HLB글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "204320.KS",
  "name": "HL만도",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "060980.KS",
  "name": "HL홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011200.KS",
  "name": "HMM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035000.KS",
  "name": "HS애드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003560.KS",
  "name": "IHQ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "175330.KS",
  "name": "JB금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "234080.KS",
  "name": "JW생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001060.KS",
  "name": "JW중외제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001067.KS",
  "name": "JW중외제약2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001065.KS",
  "name": "JW중외제약우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "096760.KS",
  "name": "JW홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "105560.KS",
  "name": "KB금융",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "432320.KS",
  "name": "KB스타리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002380.KS",
  "name": "KCC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "344820.KS",
  "name": "KCC글라스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009070.KS",
  "name": "KCTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009440.KS",
  "name": "KC그린홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "119650.KS",
  "name": "KC코트렐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092220.KS",
  "name": "KEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003620.KS",
  "name": "KG모빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016380.KS",
  "name": "KG스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001390.KS",
  "name": "KG케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033180.KS",
  "name": "KH 필룩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015590.KS",
  "name": "KIB플러그에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001940.KS",
  "name": "KISCO홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025000.KS",
  "name": "KPX케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092230.KS",
  "name": "KPX홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000040.KS",
  "name": "KR모터스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "044450.KS",
  "name": "KSS해운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030200.KS",
  "name": "KT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033780.KS",
  "name": "KT&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058850.KS",
  "name": "KTcs",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058860.KS",
  "name": "KTis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093050.KS",
  "name": "LF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003550.KS",
  "name": "LG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034220.KS",
  "name": "LG디스플레이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051900.KS",
  "name": "LG생활건강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051905.KS",
  "name": "LG생활건강우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "373220.KS",
  "name": "LG에너지솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003555.KS",
  "name": "LG우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032640.KS",
  "name": "LG유플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011070.KS",
  "name": "LG이노텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "066570.KS",
  "name": "LG전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "066575.KS",
  "name": "LG전자우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "037560.KS",
  "name": "LG헬로비전",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051910.KS",
  "name": "LG화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051915.KS",
  "name": "LG화학우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079550.KS",
  "name": "LIG넥스원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006260.KS",
  "name": "LS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010120.KS",
  "name": "LS ELECTRIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000680.KS",
  "name": "LS네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "229640.KS",
  "name": "LS에코에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "108320.KS",
  "name": "LX세미콘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001120.KS",
  "name": "LX인터내셔널",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "108670.KS",
  "name": "LX하우시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "108675.KS",
  "name": "LX하우시스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "383800.KS",
  "name": "LX홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "38380K.KS",
  "name": "LX홀딩스1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023150.KS",
  "name": "MH에탄올",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035420.KS",
  "name": "NAVER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "181710.KS",
  "name": "NHN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "400760.KS",
  "name": "NH올원리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005940.KS",
  "name": "NH투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005945.KS",
  "name": "NH투자증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "338100.KS",
  "name": "NH프라임리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034310.KS",
  "name": "NICE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030190.KS",
  "name": "NICE평가정보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008260.KS",
  "name": "NI스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004250.KS",
  "name": "NPC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004255.KS",
  "name": "NPC우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "456040.KS",
  "name": "OCI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010060.KS",
  "name": "OCI홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "178920.KS",
  "name": "PI첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005490.KS",
  "name": "POSCO홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010950.KS",
  "name": "S-Oil",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010955.KS",
  "name": "S-Oil우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034120.KS",
  "name": "SBS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005090.KS",
  "name": "SGC에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001380.KS",
  "name": "SG글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004060.KS",
  "name": "SG세계물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001770.KS",
  "name": "SHD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002360.KS",
  "name": "SH에너지화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009160.KS",
  "name": "SIMPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "123700.KS",
  "name": "SJM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025530.KS",
  "name": "SJM홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034730.KS",
  "name": "SK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011790.KS",
  "name": "SKC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018670.KS",
  "name": "SK가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001740.KS",
  "name": "SK네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006120.KS",
  "name": "SK디스커버리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006125.KS",
  "name": "SK디스커버리우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "210980.KS",
  "name": "SK디앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "395400.KS",
  "name": "SK리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "302440.KS",
  "name": "SK바이오사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "326030.KS",
  "name": "SK바이오팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "402340.KS",
  "name": "SK스퀘어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "361610.KS",
  "name": "SK아이이테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100090.KS",
  "name": "SK오션플랜트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "03473K.KS",
  "name": "SK우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "096770.KS",
  "name": "SK이노베이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "096775.KS",
  "name": "SK이노베이션우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "475150.KS",
  "name": "SK이터닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001510.KS",
  "name": "SK증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001515.KS",
  "name": "SK증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "285130.KS",
  "name": "SK케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "28513K.KS",
  "name": "SK케미칼우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017670.KS",
  "name": "SK텔레콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000660.KS",
  "name": "SK하이닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003570.KS",
  "name": "SNT다이내믹스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "064960.KS",
  "name": "SNT모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100840.KS",
  "name": "SNT에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036530.KS",
  "name": "SNT홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005610.KS",
  "name": "SPC삼립",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011810.KS",
  "name": "STX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "465770.KS",
  "name": "STX그린로지스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "077970.KS",
  "name": "STX엔진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071970.KS",
  "name": "STX중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002820.KS",
  "name": "SUN&L",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084870.KS",
  "name": "TBH글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002710.KS",
  "name": "TCC스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069260.KS",
  "name": "TKG휴켐스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002900.KS",
  "name": "TYM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024070.KS",
  "name": "WISCOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "037270.KS",
  "name": "YG PLUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000500.KS",
  "name": "가온전선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000860.KS",
  "name": "강남제비스코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035250.KS",
  "name": "강원랜드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011420.KS",
  "name": "갤럭시아에스엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002100.KS",
  "name": "경농",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009450.KS",
  "name": "경동나비엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267290.KS",
  "name": "경동도시가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012320.KS",
  "name": "경동인베스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000050.KS",
  "name": "경방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214390.KS",
  "name": "경보제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012610.KS",
  "name": "경인양행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009140.KS",
  "name": "경인전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013580.KS",
  "name": "계룡건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012200.KS",
  "name": "계양전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012205.KS",
  "name": "계양전기우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002140.KS",
  "name": "고려산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010130.KS",
  "name": "고려아연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002240.KS",
  "name": "고려제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009290.KS",
  "name": "광동제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017040.KS",
  "name": "광명전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017900.KS",
  "name": "광전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "037710.KS",
  "name": "광주신세계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030610.KS",
  "name": "교보증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "339770.KS",
  "name": "교촌에프앤비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007690.KS",
  "name": "국도화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005320.KS",
  "name": "국동",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001140.KS",
  "name": "국보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002720.KS",
  "name": "국제약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "083420.KS",
  "name": "그린케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014530.KS",
  "name": "극동유화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014280.KS",
  "name": "금강공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014285.KS",
  "name": "금강공업우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008870.KS",
  "name": "금비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001570.KS",
  "name": "금양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002990.KS",
  "name": "금호건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002995.KS",
  "name": "금호건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011780.KS",
  "name": "금호석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011785.KS",
  "name": "금호석유우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214330.KS",
  "name": "금호에이치티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001210.KS",
  "name": "금호전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "073240.KS",
  "name": "금호타이어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092440.KS",
  "name": "기신정기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000270.KS",
  "name": "기아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024110.KS",
  "name": "기업은행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013700.KS",
  "name": "까뮤이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004540.KS",
  "name": "깨끗한나라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004545.KS",
  "name": "깨끗한나라우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001260.KS",
  "name": "남광토건",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008350.KS",
  "name": "남선알미늄",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008355.KS",
  "name": "남선알미우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004270.KS",
  "name": "남성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003920.KS",
  "name": "남양유업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003925.KS",
  "name": "남양유업우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025860.KS",
  "name": "남해화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005720.KS",
  "name": "넥센",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005725.KS",
  "name": "넥센우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002350.KS",
  "name": "넥센타이어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002355.KS",
  "name": "넥센타이어1우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092790.KS",
  "name": "넥스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "251270.KS",
  "name": "넷마블",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090350.KS",
  "name": "노루페인트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090355.KS",
  "name": "노루페인트우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000320.KS",
  "name": "노루홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000325.KS",
  "name": "노루홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006280.KS",
  "name": "녹십자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005250.KS",
  "name": "녹십자홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005257.KS",
  "name": "녹십자홀딩스2우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004370.KS",
  "name": "농심",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "072710.KS",
  "name": "농심홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058730.KS",
  "name": "다스코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030210.KS",
  "name": "다올투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023590.KS",
  "name": "다우기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145210.KS",
  "name": "다이나믹디자인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019680.KS",
  "name": "대교",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019685.KS",
  "name": "대교우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006370.KS",
  "name": "대구백화점",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008060.KS",
  "name": "대덕",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00806K.KS",
  "name": "대덕1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "353200.KS",
  "name": "대덕전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "35320K.KS",
  "name": "대덕전자1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000490.KS",
  "name": "대동",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008110.KS",
  "name": "대동전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005750.KS",
  "name": "대림B&Co",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006570.KS",
  "name": "대림통상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001680.KS",
  "name": "대상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001685.KS",
  "name": "대상우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084690.KS",
  "name": "대상홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084695.KS",
  "name": "대상홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "128820.KS",
  "name": "대성산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "117580.KS",
  "name": "대성에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016710.KS",
  "name": "대성홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003540.KS",
  "name": "대신증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003547.KS",
  "name": "대신증권2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003545.KS",
  "name": "대신증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009190.KS",
  "name": "대양금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014160.KS",
  "name": "대영포장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047040.KS",
  "name": "대우건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009320.KS",
  "name": "대우부품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003090.KS",
  "name": "대웅",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069620.KS",
  "name": "대웅제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000430.KS",
  "name": "대원강업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006340.KS",
  "name": "대원전선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006345.KS",
  "name": "대원전선우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003220.KS",
  "name": "대원제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024890.KS",
  "name": "대원화성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002880.KS",
  "name": "대유에이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000300.KS",
  "name": "대유플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012800.KS",
  "name": "대창",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015230.KS",
  "name": "대창단조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001070.KS",
  "name": "대한방직",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006650.KS",
  "name": "대한유화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001440.KS",
  "name": "대한전선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084010.KS",
  "name": "대한제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001790.KS",
  "name": "대한제당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001795.KS",
  "name": "대한제당우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001130.KS",
  "name": "대한제분",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003490.KS",
  "name": "대한항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003495.KS",
  "name": "대한항공우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005880.KS",
  "name": "대한해운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003830.KS",
  "name": "대한화섬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016090.KS",
  "name": "대현",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069460.KS",
  "name": "대호에이엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192080.KS",
  "name": "더블유게임즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012510.KS",
  "name": "더존비즈온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004830.KS",
  "name": "덕성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004835.KS",
  "name": "덕성우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024900.KS",
  "name": "덕양산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145720.KS",
  "name": "덴티움",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002150.KS",
  "name": "도화엔지니어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "460850.KS",
  "name": "동국씨엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "460860.KS",
  "name": "동국제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001230.KS",
  "name": "동국홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023450.KS",
  "name": "동남합성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004140.KS",
  "name": "동방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007590.KS",
  "name": "동방아그로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005960.KS",
  "name": "동부건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005965.KS",
  "name": "동부건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "026960.KS",
  "name": "동서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002210.KS",
  "name": "동성제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "102260.KS",
  "name": "동성케미컬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000640.KS",
  "name": "동아쏘시오홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "170900.KS",
  "name": "동아에스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028100.KS",
  "name": "동아지질",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "282690.KS",
  "name": "동아타이어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001520.KS",
  "name": "동양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001527.KS",
  "name": "동양2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084670.KS",
  "name": "동양고속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "082640.KS",
  "name": "동양생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001525.KS",
  "name": "동양우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008970.KS",
  "name": "동양철관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092780.KS",
  "name": "동양피스톤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "049770.KS",
  "name": "동원F&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018500.KS",
  "name": "동원금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006040.KS",
  "name": "동원산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030720.KS",
  "name": "동원수산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014820.KS",
  "name": "동원시스템즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014825.KS",
  "name": "동원시스템즈우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "111380.KS",
  "name": "동인기연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "163560.KS",
  "name": "동일고무벨트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004890.KS",
  "name": "동일산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002690.KS",
  "name": "동일제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000020.KS",
  "name": "동화약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000150.KS",
  "name": "두산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000157.KS",
  "name": "두산2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "454910.KS",
  "name": "두산로보틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "241560.KS",
  "name": "두산밥캣",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034020.KS",
  "name": "두산에너빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000155.KS",
  "name": "두산우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "336260.KS",
  "name": "두산퓨얼셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33626K.KS",
  "name": "두산퓨얼셀1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33626L.KS",
  "name": "두산퓨얼셀2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016740.KS",
  "name": "두올",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192650.KS",
  "name": "드림텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024090.KS",
  "name": "디씨엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003160.KS",
  "name": "디아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092200.KS",
  "name": "디아이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "377190.KS",
  "name": "디앤디플랫폼리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013570.KS",
  "name": "디와이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "210540.KS",
  "name": "디와이파워",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "115390.KS",
  "name": "락앤락",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032350.KS",
  "name": "롯데관광개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "089860.KS",
  "name": "롯데렌탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "330590.KS",
  "name": "롯데리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000400.KS",
  "name": "롯데손해보험",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023530.KS",
  "name": "롯데쇼핑",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020150.KS",
  "name": "롯데에너지머티리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "280360.KS",
  "name": "롯데웰푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "286940.KS",
  "name": "롯데이노베이트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004000.KS",
  "name": "롯데정밀화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004990.KS",
  "name": "롯데지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00499K.KS",
  "name": "롯데지주우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005300.KS",
  "name": "롯데칠성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005305.KS",
  "name": "롯데칠성우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011170.KS",
  "name": "롯데케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071840.KS",
  "name": "롯데하이마트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "027740.KS",
  "name": "마니커",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "357430.KS",
  "name": "마스턴프리미어리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001080.KS",
  "name": "만호제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088980.KS",
  "name": "맥쿼리인프라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "094800.KS",
  "name": "맵스리얼티1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "138040.KS",
  "name": "메리츠금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090370.KS",
  "name": "메타랩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017180.KS",
  "name": "명문제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009900.KS",
  "name": "명신산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012690.KS",
  "name": "모나리자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005360.KS",
  "name": "모나미",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009680.KS",
  "name": "모토닉",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009580.KS",
  "name": "무림P&P",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009200.KS",
  "name": "무림페이퍼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033920.KS",
  "name": "무학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008420.KS",
  "name": "문배철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025560.KS",
  "name": "미래산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007120.KS",
  "name": "미래아이앤지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "396690.KS",
  "name": "미래에셋글로벌리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "357250.KS",
  "name": "미래에셋맵스리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "085620.KS",
  "name": "미래에셋생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006800.KS",
  "name": "미래에셋증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00680K.KS",
  "name": "미래에셋증권2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006805.KS",
  "name": "미래에셋증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002840.KS",
  "name": "미원상사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "268280.KS",
  "name": "미원에스씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "107590.KS",
  "name": "미원홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "134380.KS",
  "name": "미원화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003650.KS",
  "name": "미창석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "377740.KS",
  "name": "바이오노트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003610.KS",
  "name": "방림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001340.KS",
  "name": "백광산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035150.KS",
  "name": "백산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002410.KS",
  "name": "범양건영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007210.KS",
  "name": "벽산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002760.KS",
  "name": "보락",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003850.KS",
  "name": "보령",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000890.KS",
  "name": "보해양조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003000.KS",
  "name": "부광약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001270.KS",
  "name": "부국증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001275.KS",
  "name": "부국증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "026940.KS",
  "name": "부국철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011390.KS",
  "name": "부산산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005030.KS",
  "name": "부산주공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002070.KS",
  "name": "비비안",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100220.KS",
  "name": "비상교육",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090460.KS",
  "name": "비에이치",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030790.KS",
  "name": "비케이탑스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005180.KS",
  "name": "빙그레",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003960.KS",
  "name": "사조대림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008040.KS",
  "name": "사조동아원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007160.KS",
  "name": "사조산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014710.KS",
  "name": "사조씨푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006090.KS",
  "name": "사조오양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001470.KS",
  "name": "삼부토건",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028050.KS",
  "name": "삼성E&A",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "448730.KS",
  "name": "삼성FN리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006400.KS",
  "name": "삼성SDI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006405.KS",
  "name": "삼성SDI우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006660.KS",
  "name": "삼성공조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028260.KS",
  "name": "삼성물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "02826K.KS",
  "name": "삼성물산우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "207940.KS",
  "name": "삼성바이오로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032830.KS",
  "name": "삼성생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018260.KS",
  "name": "삼성에스디에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009150.KS",
  "name": "삼성전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009155.KS",
  "name": "삼성전기우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005930.KS",
  "name": "삼성전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005935.KS",
  "name": "삼성전자우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001360.KS",
  "name": "삼성제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010140.KS",
  "name": "삼성중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016360.KS",
  "name": "삼성증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "068290.KS",
  "name": "삼성출판사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "029780.KS",
  "name": "삼성카드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000810.KS",
  "name": "삼성화재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000815.KS",
  "name": "삼성화재우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006110.KS",
  "name": "삼아알미늄",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145990.KS",
  "name": "삼양사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145995.KS",
  "name": "삼양사우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003230.KS",
  "name": "삼양식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002170.KS",
  "name": "삼양통상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "272550.KS",
  "name": "삼양패키징",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000070.KS",
  "name": "삼양홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000075.KS",
  "name": "삼양홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003720.KS",
  "name": "삼영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002810.KS",
  "name": "삼영무역",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005680.KS",
  "name": "삼영전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023000.KS",
  "name": "삼원강재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004380.KS",
  "name": "삼익THK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002450.KS",
  "name": "삼익악기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004440.KS",
  "name": "삼일씨엔에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000520.KS",
  "name": "삼일제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009770.KS",
  "name": "삼정펄프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005500.KS",
  "name": "삼진제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004690.KS",
  "name": "삼천리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010960.KS",
  "name": "삼호개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004450.KS",
  "name": "삼화왕관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009470.KS",
  "name": "삼화전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011230.KS",
  "name": "삼화전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001820.KS",
  "name": "삼화콘덴서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000390.KS",
  "name": "삼화페인트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001290.KS",
  "name": "상상인증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "041650.KS",
  "name": "상신브레이크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "075180.KS",
  "name": "새론오토모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007540.KS",
  "name": "샘표",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "248170.KS",
  "name": "샘표식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007860.KS",
  "name": "서연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "200880.KS",
  "name": "서연이화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017390.KS",
  "name": "서울가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004410.KS",
  "name": "서울식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004415.KS",
  "name": "서울식품우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "021050.KS",
  "name": "서원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008490.KS",
  "name": "서흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007610.KS",
  "name": "선도전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "136490.KS",
  "name": "선진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014910.KS",
  "name": "성문전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014915.KS",
  "name": "성문전자우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003080.KS",
  "name": "성보화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004980.KS",
  "name": "성신양회",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004985.KS",
  "name": "성신양회우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011300.KS",
  "name": "성안머티리얼스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000180.KS",
  "name": "성창기업지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002420.KS",
  "name": "세기상사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004360.KS",
  "name": "세방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004365.KS",
  "name": "세방우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004490.KS",
  "name": "세방전지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001430.KS",
  "name": "세아베스틸지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "306200.KS",
  "name": "세아제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003030.KS",
  "name": "세아제강지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019440.KS",
  "name": "세아특수강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058650.KS",
  "name": "세아홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013000.KS",
  "name": "세우글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "091090.KS",
  "name": "세원이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "021820.KS",
  "name": "세원정공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "067830.KS",
  "name": "세이브존I&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033530.KS",
  "name": "세종공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "075580.KS",
  "name": "세진중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "068270.KS",
  "name": "셀트리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "336370.KS",
  "name": "솔루스첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33637K.KS",
  "name": "솔루스첨단소재1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33637L.KS",
  "name": "솔루스첨단소재2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "248070.KS",
  "name": "솔루엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004430.KS",
  "name": "송원산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "126720.KS",
  "name": "수산인더스트리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017550.KS",
  "name": "수산중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "053210.KS",
  "name": "스카이라이프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "204210.KS",
  "name": "스타리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "026890.KS",
  "name": "스틱인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "134790.KS",
  "name": "시디즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016590.KS",
  "name": "신대양제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "029530.KS",
  "name": "신도리코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004970.KS",
  "name": "신라교역",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011930.KS",
  "name": "신성이엔지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005390.KS",
  "name": "신성통상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004170.KS",
  "name": "신세계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035510.KS",
  "name": "신세계 I&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034300.KS",
  "name": "신세계건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "031430.KS",
  "name": "신세계인터내셔날",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "031440.KS",
  "name": "신세계푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006880.KS",
  "name": "신송홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005800.KS",
  "name": "신영와코루",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001720.KS",
  "name": "신영증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001725.KS",
  "name": "신영증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009270.KS",
  "name": "신원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002700.KS",
  "name": "신일전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002870.KS",
  "name": "신풍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019170.KS",
  "name": "신풍제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019175.KS",
  "name": "신풍제약우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "404990.KS",
  "name": "신한서부티엔디리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "293940.KS",
  "name": "신한알파리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "055550.KS",
  "name": "신한지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004080.KS",
  "name": "신흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "102280.KS",
  "name": "쌍방울",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003410.KS",
  "name": "쌍용C&E",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004770.KS",
  "name": "써니전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "403550.KS",
  "name": "쏘카",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004920.KS",
  "name": "씨아이테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "112610.KS",
  "name": "씨에스윈드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "308170.KS",
  "name": "씨티알모빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008700.KS",
  "name": "아남전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002790.KS",
  "name": "아모레G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00279K.KS",
  "name": "아모레G3우(전환)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002795.KS",
  "name": "아모레G우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090430.KS",
  "name": "아모레퍼시픽",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090435.KS",
  "name": "아모레퍼시픽우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002030.KS",
  "name": "아세아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "183190.KS",
  "name": "아세아시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002310.KS",
  "name": "아세아제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012170.KS",
  "name": "아센디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267850.KS",
  "name": "아시아나IDT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020560.KS",
  "name": "아시아나항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "122900.KS",
  "name": "아이마켓코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010780.KS",
  "name": "아이에스동서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "139990.KS",
  "name": "아주스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001780.KS",
  "name": "알루코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018250.KS",
  "name": "애경산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "161000.KS",
  "name": "애경케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011090.KS",
  "name": "에넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "137310.KS",
  "name": "에스디바이오센서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "118000.KS",
  "name": "에스메디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005850.KS",
  "name": "에스엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010580.KS",
  "name": "에스엠벡셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012750.KS",
  "name": "에스원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023960.KS",
  "name": "에쓰씨엔지니어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298690.KS",
  "name": "에어부산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "140910.KS",
  "name": "에이리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078520.KS",
  "name": "에이블씨엔씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015260.KS",
  "name": "에이엔피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007460.KS",
  "name": "에이프로젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003060.KS",
  "name": "에이프로젠바이오로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "244920.KS",
  "name": "에이플러스에셋",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "278470.KS",
  "name": "에이피알",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "450080.KS",
  "name": "에코프로머티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036570.KS",
  "name": "엔씨소프트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "085310.KS",
  "name": "엔케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "900140.KS",
  "name": "엘브이엠씨홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "066970.KS",
  "name": "엘앤에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097520.KS",
  "name": "엠씨넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014440.KS",
  "name": "영보화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "111770.KS",
  "name": "영원무역",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009970.KS",
  "name": "영원무역홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003520.KS",
  "name": "영진약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000670.KS",
  "name": "영풍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006740.KS",
  "name": "영풍제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012280.KS",
  "name": "영화금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012160.KS",
  "name": "영흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015360.KS",
  "name": "예스코홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007310.KS",
  "name": "오뚜기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002630.KS",
  "name": "오리엔트바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "271560.KS",
  "name": "오리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001800.KS",
  "name": "오리온홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011690.KS",
  "name": "와이투솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "070960.KS",
  "name": "용평리조트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "316140.KS",
  "name": "우리금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006980.KS",
  "name": "우성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017370.KS",
  "name": "우신시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "105840.KS",
  "name": "우진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010400.KS",
  "name": "우진아이엔에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "049800.KS",
  "name": "우진플라임",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016880.KS",
  "name": "웅진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "095720.KS",
  "name": "웅진씽크빅",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005820.KS",
  "name": "원림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010600.KS",
  "name": "웰바이오텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008600.KS",
  "name": "윌비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033270.KS",
  "name": "유나이티드제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014830.KS",
  "name": "유니드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "446070.KS",
  "name": "유니드비티플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000910.KS",
  "name": "유니온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047400.KS",
  "name": "유니온머티리얼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011330.KS",
  "name": "유니켐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "077500.KS",
  "name": "유니퀘스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002920.KS",
  "name": "유성기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000700.KS",
  "name": "유수홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003470.KS",
  "name": "유안타증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003475.KS",
  "name": "유안타증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "072130.KS",
  "name": "유엔젤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000220.KS",
  "name": "유유제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000225.KS",
  "name": "유유제약1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000227.KS",
  "name": "유유제약2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001200.KS",
  "name": "유진투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000100.KS",
  "name": "유한양행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000105.KS",
  "name": "유한양행우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003460.KS",
  "name": "유화증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003465.KS",
  "name": "유화증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008730.KS",
  "name": "율촌화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008250.KS",
  "name": "이건산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025820.KS",
  "name": "이구산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214320.KS",
  "name": "이노션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088260.KS",
  "name": "이리츠코크렙",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "139480.KS",
  "name": "이마트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "457190.KS",
  "name": "이수스페셜티케미컬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007660.KS",
  "name": "이수페타시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005950.KS",
  "name": "이수화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015020.KS",
  "name": "이스타코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093230.KS",
  "name": "이아이디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "074610.KS",
  "name": "이엔플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "102460.KS",
  "name": "이연제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084680.KS",
  "name": "이월드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "350520.KS",
  "name": "이지스레지던스리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "334890.KS",
  "name": "이지스밸류리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000760.KS",
  "name": "이화산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014990.KS",
  "name": "인디에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "101140.KS",
  "name": "인바이오젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006490.KS",
  "name": "인스코비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023800.KS",
  "name": "인지컨트롤스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034590.KS",
  "name": "인천도시가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "129260.KS",
  "name": "인터지스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023810.KS",
  "name": "인팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "249420.KS",
  "name": "일동제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000230.KS",
  "name": "일동홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013360.KS",
  "name": "일성건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003120.KS",
  "name": "일성아이에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003200.KS",
  "name": "일신방직",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007110.KS",
  "name": "일신석재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007570.KS",
  "name": "일양약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007575.KS",
  "name": "일양약품우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008500.KS",
  "name": "일정실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "081000.KS",
  "name": "일진다이아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020760.KS",
  "name": "일진디스플",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "103590.KS",
  "name": "일진전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "271940.KS",
  "name": "일진하이솔루스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015860.KS",
  "name": "일진홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "226320.KS",
  "name": "잇츠한불",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "317400.KS",
  "name": "자이에스앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033240.KS",
  "name": "자화전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000950.KS",
  "name": "전방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "348950.KS",
  "name": "제이알글로벌리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "194370.KS",
  "name": "제이에스코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025620.KS",
  "name": "제이준코스메틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030000.KS",
  "name": "제일기획",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "271980.KS",
  "name": "제일약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001560.KS",
  "name": "제일연마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002620.KS",
  "name": "제일파마홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006220.KS",
  "name": "제주은행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "089590.KS",
  "name": "제주항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004910.KS",
  "name": "조광페인트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004700.KS",
  "name": "조광피혁",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001550.KS",
  "name": "조비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "462520.KS",
  "name": "조선내화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "120030.KS",
  "name": "조선선재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018470.KS",
  "name": "조일알미늄",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002600.KS",
  "name": "조흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "185750.KS",
  "name": "종근당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "063160.KS",
  "name": "종근당바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001630.KS",
  "name": "종근당홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "109070.KS",
  "name": "주성코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "044380.KS",
  "name": "주연테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013890.KS",
  "name": "지누스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013870.KS",
  "name": "지엠비코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071320.KS",
  "name": "지역난방공사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088790.KS",
  "name": "진도",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003780.KS",
  "name": "진양산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010640.KS",
  "name": "진양폴리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100250.KS",
  "name": "진양홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051630.KS",
  "name": "진양화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "272450.KS",
  "name": "진에어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011000.KS",
  "name": "진원생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002780.KS",
  "name": "진흥기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002787.KS",
  "name": "진흥기업2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002785.KS",
  "name": "진흥기업우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009310.KS",
  "name": "참엔지니어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000650.KS",
  "name": "천일고속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012600.KS",
  "name": "청호ICT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033250.KS",
  "name": "체시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035720.KS",
  "name": "카카오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "323410.KS",
  "name": "카카오뱅크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "377300.KS",
  "name": "카카오페이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006380.KS",
  "name": "카프로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001620.KS",
  "name": "케이비아이동국실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "029460.KS",
  "name": "케이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "281820.KS",
  "name": "케이씨텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "381970.KS",
  "name": "케이카",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145270.KS",
  "name": "케이탑리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "417310.KS",
  "name": "코람코더원리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "357120.KS",
  "name": "코람코라이프인프라리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007815.KS",
  "name": "코리아써우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007810.KS",
  "name": "코리아써키트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00781K.KS",
  "name": "코리아써키트2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003690.KS",
  "name": "코리안리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192820.KS",
  "name": "코스맥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "044820.KS",
  "name": "코스맥스비티아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005070.KS",
  "name": "코스모신소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005420.KS",
  "name": "코스모화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071950.KS",
  "name": "코아스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002020.KS",
  "name": "코오롱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003070.KS",
  "name": "코오롱글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003075.KS",
  "name": "코오롱글로벌우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "450140.KS",
  "name": "코오롱모빌리티그룹",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "45014K.KS",
  "name": "코오롱모빌리티그룹우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002025.KS",
  "name": "코오롱우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "120110.KS",
  "name": "코오롱인더",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "120115.KS",
  "name": "코오롱인더우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "138490.KS",
  "name": "코오롱플라스틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "021240.KS",
  "name": "코웨이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036420.KS",
  "name": "콘텐트리중앙",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024720.KS",
  "name": "콜마홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "031820.KS",
  "name": "콤텍시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192400.KS",
  "name": "쿠쿠홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "284740.KS",
  "name": "쿠쿠홈시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "264900.KS",
  "name": "크라운제과",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "26490K.KS",
  "name": "크라운제과우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005740.KS",
  "name": "크라운해태홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005745.KS",
  "name": "크라운해태홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "259960.KS",
  "name": "크래프톤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020120.KS",
  "name": "키다리스튜디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "039490.KS",
  "name": "키움증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014580.KS",
  "name": "태경비케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015890.KS",
  "name": "태경산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006890.KS",
  "name": "태경케미컬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003240.KS",
  "name": "태광산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011280.KS",
  "name": "태림포장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004100.KS",
  "name": "태양금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004105.KS",
  "name": "태양금속우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009410.KS",
  "name": "태영건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009415.KS",
  "name": "태영건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001420.KS",
  "name": "태원물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007980.KS",
  "name": "태평양물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "055490.KS",
  "name": "테이팩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078000.KS",
  "name": "텔코웨어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214420.KS",
  "name": "토니모리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019180.KS",
  "name": "티에이치엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "363280.KS",
  "name": "티와이홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "36328K.KS",
  "name": "티와이홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "091810.KS",
  "name": "티웨이항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004870.KS",
  "name": "티웨이홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005690.KS",
  "name": "파미셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036580.KS",
  "name": "팜스코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004720.KS",
  "name": "팜젠사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028670.KS",
  "name": "팬오션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010820.KS",
  "name": "퍼스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016800.KS",
  "name": "퍼시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001020.KS",
  "name": "페이퍼코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090080.KS",
  "name": "평화산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010770.KS",
  "name": "평화홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "022100.KS",
  "name": "포스코DX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058430.KS",
  "name": "포스코스틸리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047050.KS",
  "name": "포스코인터내셔널",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003670.KS",
  "name": "포스코퓨처엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017810.KS",
  "name": "풀무원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "103140.KS",
  "name": "풍산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005810.KS",
  "name": "풍산홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "950210.KS",
  "name": "프레스티지바이오파마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009810.KS",
  "name": "플레이그램",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "086790.KS",
  "name": "하나금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "293480.KS",
  "name": "하나제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "039130.KS",
  "name": "하나투어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "352820.KS",
  "name": "하이브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071090.KS",
  "name": "하이스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019490.KS",
  "name": "하이트론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000080.KS",
  "name": "하이트진로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000087.KS",
  "name": "하이트진로2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000140.KS",
  "name": "하이트진로홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000145.KS",
  "name": "하이트진로홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "152550.KS",
  "name": "한국ANKOR유전",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036460.KS",
  "name": "한국가스공사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005430.KS",
  "name": "한국공항",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071050.KS",
  "name": "한국금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071055.KS",
  "name": "한국금융지주우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010040.KS",
  "name": "한국내화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025540.KS",
  "name": "한국단자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010100.KS",
  "name": "한국무브넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004090.KS",
  "name": "한국석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002200.KS",
  "name": "한국수출포장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002960.KS",
  "name": "한국쉘석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000240.KS",
  "name": "한국앤컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "123890.KS",
  "name": "한국자산신탁",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015760.KS",
  "name": "한국전력",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006200.KS",
  "name": "한국전자홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "027970.KS",
  "name": "한국제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023350.KS",
  "name": "한국종합기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025890.KS",
  "name": "한국주강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000970.KS",
  "name": "한국주철관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "104700.KS",
  "name": "한국철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017960.KS",
  "name": "한국카본",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "161890.KS",
  "name": "한국콜마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "161390.KS",
  "name": "한국타이어앤테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034830.KS",
  "name": "한국토지신탁",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007280.KS",
  "name": "한국특강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "168490.KS",
  "name": "한국패러랠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047810.KS",
  "name": "한국항공우주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "123690.KS",
  "name": "한국화장품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003350.KS",
  "name": "한국화장품제조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011500.KS",
  "name": "한농화성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002390.KS",
  "name": "한독",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "053690.KS",
  "name": "한미글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "042700.KS",
  "name": "한미반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008930.KS",
  "name": "한미사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "128940.KS",
  "name": "한미약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009240.KS",
  "name": "한샘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020000.KS",
  "name": "한섬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003680.KS",
  "name": "한성기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "105630.KS",
  "name": "한세실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069640.KS",
  "name": "한세엠케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016450.KS",
  "name": "한세예스24홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010420.KS",
  "name": "한솔PNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009180.KS",
  "name": "한솔로지스틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "213500.KS",
  "name": "한솔제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014680.KS",
  "name": "한솔케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004710.KS",
  "name": "한솔테크닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004150.KS",
  "name": "한솔홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025750.KS",
  "name": "한솔홈데코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004960.KS",
  "name": "한신공영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011700.KS",
  "name": "한신기계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001750.KS",
  "name": "한양증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001755.KS",
  "name": "한양증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018880.KS",
  "name": "한온시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009420.KS",
  "name": "한올바이오파마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014130.KS",
  "name": "한익스프레스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "300720.KS",
  "name": "한일시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002220.KS",
  "name": "한일철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006390.KS",
  "name": "한일현대시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003300.KS",
  "name": "한일홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051600.KS",
  "name": "한전KPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "052690.KS",
  "name": "한전기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "130660.KS",
  "name": "한전산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002320.KS",
  "name": "한진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003480.KS",
  "name": "한진중공업홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "180640.KS",
  "name": "한진칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "18064K.KS",
  "name": "한진칼우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005110.KS",
  "name": "한창",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009460.KS",
  "name": "한창제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "372910.KS",
  "name": "한컴라이프케어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000880.KS",
  "name": "한화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00088K.KS",
  "name": "한화3우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "452260.KS",
  "name": "한화갤러리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "45226K.KS",
  "name": "한화갤러리아우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "451800.KS",
  "name": "한화리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088350.KS",
  "name": "한화생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000370.KS",
  "name": "한화손해보험",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009830.KS",
  "name": "한화솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009835.KS",
  "name": "한화솔루션우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "272210.KS",
  "name": "한화시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012450.KS",
  "name": "한화에어로스페이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "082740.KS",
  "name": "한화엔진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "042660.KS",
  "name": "한화오션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000885.KS",
  "name": "한화우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003530.KS",
  "name": "한화투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003535.KS",
  "name": "한화투자증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "195870.KS",
  "name": "해성디에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "101530.KS",
  "name": "해태제과식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "143210.KS",
  "name": "핸즈코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000720.KS",
  "name": "현대건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000725.KS",
  "name": "현대건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "453340.KS",
  "name": "현대그린푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "086280.KS",
  "name": "현대글로비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "064350.KS",
  "name": "현대로템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079430.KS",
  "name": "현대리바트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012330.KS",
  "name": "현대모비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069960.KS",
  "name": "현대백화점",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004560.KS",
  "name": "현대비앤지스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004310.KS",
  "name": "현대약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017800.KS",
  "name": "현대엘리베이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "307950.KS",
  "name": "현대오토에버",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011210.KS",
  "name": "현대위아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004020.KS",
  "name": "현대제철",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005440.KS",
  "name": "현대지에프홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005380.KS",
  "name": "현대차",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005387.KS",
  "name": "현대차2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005389.KS",
  "name": "현대차3우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005385.KS",
  "name": "현대차우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001500.KS",
  "name": "현대차증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011760.KS",
  "name": "현대코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "227840.KS",
  "name": "현대코퍼레이션홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "126560.KS",
  "name": "현대퓨처넷",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001450.KS",
  "name": "현대해상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "057050.KS",
  "name": "현대홈쇼핑",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093240.KS",
  "name": "형지엘리트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003010.KS",
  "name": "혜인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "111110.KS",
  "name": "호전실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008770.KS",
  "name": "호텔신라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008775.KS",
  "name": "호텔신라우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002460.KS",
  "name": "화성산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "378850.KS",
  "name": "화승알앤에이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "241590.KS",
  "name": "화승엔터프라이즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006060.KS",
  "name": "화승인더",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013520.KS",
  "name": "화승코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010690.KS",
  "name": "화신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "133820.KS",
  "name": "화인베스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010660.KS",
  "name": "화천기계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000850.KS",
  "name": "화천기공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016580.KS",
  "name": "환인제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032560.KS",
  "name": "황금에스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004800.KS",
  "name": "효성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "094280.KS",
  "name": "효성ITX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298040.KS",
  "name": "효성중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298050.KS",
  "name": "효성첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298020.KS",
  "name": "효성티앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298000.KS",
  "name": "효성화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093370.KS",
  "name": "후성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "081660.KS",
  "name": "휠라홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005870.KS",
  "name": "휴니드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079980.KS",
  "name": "휴비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005010.KS",
  "name": "휴스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000540.KS",
  "name": "흥국화재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000545.KS",
  "name": "흥국화재우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003280.KS",
  "name": "흥아해운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "060310.KQ",
  "name": "3S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054620.KQ",
  "name": "APS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "265520.KQ",
  "name": "AP시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "211270.KQ",
  "name": "AP위성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109960.KQ",
  "name": "AP헬스케어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "139050.KQ",
  "name": "BF랩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126600.KQ",
  "name": "BGF에코머티리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013720.KQ",
  "name": "CBI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083790.KQ",
  "name": "CG인바이츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035760.KQ",
  "name": "CJ ENM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "311690.KQ",
  "name": "CJ 바이오사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051500.KQ",
  "name": "CJ프레시웨이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058820.KQ",
  "name": "CMG제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023460.KQ",
  "name": "CNH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056730.KQ",
  "name": "CNT85",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065770.KQ",
  "name": "CS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083660.KQ",
  "name": "CSA 코스믹",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "456440.KQ",
  "name": "DB금융스팩11호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060900.KQ",
  "name": "DGP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290120.KQ",
  "name": "DH오토리드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025440.KQ",
  "name": "DH오토웨어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068790.KQ",
  "name": "DMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241520.KQ",
  "name": "DSC인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "180400.KQ",
  "name": "DXVX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "245620.KQ",
  "name": "EDGC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037370.KQ",
  "name": "EG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050120.KQ",
  "name": "ES큐브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214270.KQ",
  "name": "FSN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "130500.KQ",
  "name": "GH신소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900290.KQ",
  "name": "GRT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083450.KQ",
  "name": "GST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "297890.KQ",
  "name": "HB솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440290.KQ",
  "name": "HB인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078150.KQ",
  "name": "HB테크놀러지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "195940.KQ",
  "name": "HK이노엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "028300.KQ",
  "name": "HLB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "278650.KQ",
  "name": "HLB바이오스텝",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067630.KQ",
  "name": "HLB생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024850.KQ",
  "name": "HLB이노베이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047920.KQ",
  "name": "HLB제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115450.KQ",
  "name": "HLB테라퓨틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046210.KQ",
  "name": "HLB파나진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "403870.KQ",
  "name": "HPSP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036640.KQ",
  "name": "HRS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439730.KQ",
  "name": "IBKS제20호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442770.KQ",
  "name": "IBKS제21호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448760.KQ",
  "name": "IBKS제22호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "467930.KQ",
  "name": "IBKS제23호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "469480.KQ",
  "name": "IBKS제24호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095340.KQ",
  "name": "ISC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099520.KQ",
  "name": "ITX-AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950170.KQ",
  "name": "JTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067290.KQ",
  "name": "JW신약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035900.KQ",
  "name": "JYP Ent.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318000.KQ",
  "name": "KBG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024840.KQ",
  "name": "KBI메탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024120.KQ",
  "name": "KB오토시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455250.KQ",
  "name": "KB제25호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "458320.KQ",
  "name": "KB제26호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "464680.KQ",
  "name": "KB제27호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021320.KQ",
  "name": "KCC건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036670.KQ",
  "name": "KCI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044180.KQ",
  "name": "KD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046440.KQ",
  "name": "KG모빌리언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035600.KQ",
  "name": "KG이니시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226360.KQ",
  "name": "KH 건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "111870.KQ",
  "name": "KH 전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060720.KQ",
  "name": "KH바텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058400.KQ",
  "name": "KNN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122450.KQ",
  "name": "KX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052900.KQ",
  "name": "KX하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376190.KQ",
  "name": "LB루셈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "061970.KQ",
  "name": "LB세미콘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "309960.KQ",
  "name": "LB인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225190.KQ",
  "name": "LK삼양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060370.KQ",
  "name": "LS마린솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417200.KQ",
  "name": "LS머트리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086960.KQ",
  "name": "MDS테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038340.KQ",
  "name": "MIT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "160550.KQ",
  "name": "NEW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053290.KQ",
  "name": "NE능률",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060250.KQ",
  "name": "NHN KCP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104200.KQ",
  "name": "NHN벅스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222160.KQ",
  "name": "NPX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024940.KQ",
  "name": "PN풍년",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "218410.KQ",
  "name": "RFHIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "327260.KQ",
  "name": "RF머트리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091340.KQ",
  "name": "S&K폴리텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419530.KQ",
  "name": "SAMG엔터",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019550.KQ",
  "name": "SBI인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950110.KQ",
  "name": "SBI핀테크솔루션즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036120.KQ",
  "name": "SCI평가정보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246960.KQ",
  "name": "SCL사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099220.KQ",
  "name": "SDN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036540.KQ",
  "name": "SFA반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "255220.KQ",
  "name": "SG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040610.KQ",
  "name": "SG&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049470.KQ",
  "name": "SGA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "184230.KQ",
  "name": "SGA솔루션즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016250.KQ",
  "name": "SGC E&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048550.KQ",
  "name": "SM C&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063440.KQ",
  "name": "SM Life Design",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067160.KQ",
  "name": "SOOP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "289080.KQ",
  "name": "SV인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089230.KQ",
  "name": "THE E&M",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "161570.KQ",
  "name": "THE MIDONG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032540.KQ",
  "name": "TJ미디어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "022220.KQ",
  "name": "TKG애강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048770.KQ",
  "name": "TPC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246690.KQ",
  "name": "TS인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317240.KQ",
  "name": "TS트릴리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "057030.KQ",
  "name": "YBM넷",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040300.KQ",
  "name": "YTN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051390.KQ",
  "name": "YW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052220.KQ",
  "name": "iMBC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079940.KQ",
  "name": "가비아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078890.KQ",
  "name": "가온그룹",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "399720.KQ",
  "name": "가온칩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036620.KQ",
  "name": "감성코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217730.KQ",
  "name": "강스템바이오텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114190.KQ",
  "name": "강원에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094480.KQ",
  "name": "갤럭시아머니트리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039240.KQ",
  "name": "경남스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053950.KQ",
  "name": "경남제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011040.KQ",
  "name": "경동제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024910.KQ",
  "name": "경창산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "198440.KQ",
  "name": "고려시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049720.KQ",
  "name": "고려신용정보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014570.KQ",
  "name": "고려제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348150.KQ",
  "name": "고바이오랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950190.KQ",
  "name": "고스트스튜디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "098460.KQ",
  "name": "고영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035290.KQ",
  "name": "골드앤에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900280.KQ",
  "name": "골든센츄리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215000.KQ",
  "name": "골프존",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121440.KQ",
  "name": "골프존뉴딘홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "366030.KQ",
  "name": "공구우먼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014200.KQ",
  "name": "광림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "029480.KQ",
  "name": "광무",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "026910.KQ",
  "name": "광진실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "421800.KQ",
  "name": "교보12호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440790.KQ",
  "name": "교보13호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "456490.KQ",
  "name": "교보14호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "465320.KQ",
  "name": "교보15호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053270.KQ",
  "name": "구영테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066620.KQ",
  "name": "국보디자인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043650.KQ",
  "name": "국순당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006050.KQ",
  "name": "국영지앤엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060480.KQ",
  "name": "국일신동",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078130.KQ",
  "name": "국일제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307750.KQ",
  "name": "국전약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035080.KQ",
  "name": "그래디언트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204020.KQ",
  "name": "그리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "402490.KQ",
  "name": "그린리소스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114450.KQ",
  "name": "그린생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "186230.KQ",
  "name": "그린플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900070.KQ",
  "name": "글로벌에스엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204620.KQ",
  "name": "글로벌텍스프리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019660.KQ",
  "name": "글로본",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053260.KQ",
  "name": "금강철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "282720.KQ",
  "name": "금양그린파워",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036190.KQ",
  "name": "금화피에스시",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049080.KQ",
  "name": "기가레인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "420770.KQ",
  "name": "기가비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035460.KQ",
  "name": "기산텔레콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "308100.KQ",
  "name": "까스텔바작",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "407400.KQ",
  "name": "꿈비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187790.KQ",
  "name": "나노",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "286750.KQ",
  "name": "나노브릭",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121600.KQ",
  "name": "나노신소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "247660.KQ",
  "name": "나노씨엠에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039860.KQ",
  "name": "나노엔텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091970.KQ",
  "name": "나노캠텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417010.KQ",
  "name": "나노팀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "405920.KQ",
  "name": "나라셀라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051490.KQ",
  "name": "나라엠앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "137080.KQ",
  "name": "나래나노텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "190510.KQ",
  "name": "나무가",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "242040.KQ",
  "name": "나무기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089600.KQ",
  "name": "나스미디어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "293580.KQ",
  "name": "나우IB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138610.KQ",
  "name": "나이벡",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "130580.KQ",
  "name": "나이스디앤비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036800.KQ",
  "name": "나이스정보통신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "267320.KQ",
  "name": "나인테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "111710.KQ",
  "name": "남화산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091590.KQ",
  "name": "남화토건",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "168330.KQ",
  "name": "내츄럴엔도텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094860.KQ",
  "name": "네오리진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "253590.KQ",
  "name": "네오셈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "212560.KQ",
  "name": "네오오토",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095660.KQ",
  "name": "네오위즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042420.KQ",
  "name": "네오위즈홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950220.KQ",
  "name": "네오이뮨텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "311390.KQ",
  "name": "네오크레마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085910.KQ",
  "name": "네오티스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092730.KQ",
  "name": "네오팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290660.KQ",
  "name": "네오펙트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "306620.KQ",
  "name": "네온테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "153460.KQ",
  "name": "네이블",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007390.KQ",
  "name": "네이처셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033640.KQ",
  "name": "네패스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "330860.KQ",
  "name": "네패스아크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089140.KQ",
  "name": "넥스턴바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "137940.KQ",
  "name": "넥스트아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "396270.KQ",
  "name": "넥스트칩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348210.KQ",
  "name": "넥스틴",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225570.KQ",
  "name": "넥슨게임즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217270.KQ",
  "name": "넵튠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104620.KQ",
  "name": "노랑풍선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "194700.KQ",
  "name": "노바렉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "285490.KQ",
  "name": "노바텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "106520.KQ",
  "name": "노블엠앤비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376930.KQ",
  "name": "노을",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "142280.KQ",
  "name": "녹십자엠에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234690.KQ",
  "name": "녹십자웰빙",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065560.KQ",
  "name": "녹원씨엔아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054050.KQ",
  "name": "농우바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069140.KQ",
  "name": "누리플랜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040160.KQ",
  "name": "누리플렉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "332290.KQ",
  "name": "누보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348340.KQ",
  "name": "뉴로메카",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060260.KQ",
  "name": "뉴보텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123840.KQ",
  "name": "뉴온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012340.KQ",
  "name": "뉴인텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214870.KQ",
  "name": "뉴지랩파마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "270870.KQ",
  "name": "뉴트리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "144960.KQ",
  "name": "뉴파워프라즈마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085670.KQ",
  "name": "뉴프렉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064260.KQ",
  "name": "다날",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340360.KQ",
  "name": "다보링크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039560.KQ",
  "name": "다산네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "154040.KQ",
  "name": "다산솔루에타",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032190.KQ",
  "name": "다우데이타",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068240.KQ",
  "name": "다원시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "020400.KQ",
  "name": "대동금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008830.KQ",
  "name": "대동기어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048470.KQ",
  "name": "대동스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "004780.KQ",
  "name": "대륙제관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017650.KQ",
  "name": "대림제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007720.KQ",
  "name": "대명소노시즌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389260.KQ",
  "name": "대명에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317850.KQ",
  "name": "대모",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290670.KQ",
  "name": "대보마그네틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078140.KQ",
  "name": "대봉엘에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065150.KQ",
  "name": "대산F&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036480.KQ",
  "name": "대성미생물",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027830.KQ",
  "name": "대성창투",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104040.KQ",
  "name": "대성파인텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "129920.KQ",
  "name": "대성하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "438220.KQ",
  "name": "대신밸런스제13호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442310.KQ",
  "name": "대신밸런스제14호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457390.KQ",
  "name": "대신밸런스제15호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457630.KQ",
  "name": "대신밸런스제16호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "471050.KQ",
  "name": "대신밸런스제17호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "020180.KQ",
  "name": "대신정보통신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045390.KQ",
  "name": "대아티아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108380.KQ",
  "name": "대양전기공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006580.KQ",
  "name": "대양제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007680.KQ",
  "name": "대원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048910.KQ",
  "name": "대원미디어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005710.KQ",
  "name": "대원산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290380.KQ",
  "name": "대유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "120240.KQ",
  "name": "대정화금",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003310.KQ",
  "name": "대주산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078600.KQ",
  "name": "대주전자재료",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096350.KQ",
  "name": "대창솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140520.KQ",
  "name": "대창스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131220.KQ",
  "name": "대한과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010170.KQ",
  "name": "대한광통신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054670.KQ",
  "name": "대한뉴팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023910.KQ",
  "name": "대한약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021040.KQ",
  "name": "대호특수강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021045.KQ",
  "name": "대호특수강우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067080.KQ",
  "name": "대화제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298540.KQ",
  "name": "더네이쳐홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032860.KQ",
  "name": "더라미",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "393890.KQ",
  "name": "더블유씨피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299170.KQ",
  "name": "더블유에스아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "224060.KQ",
  "name": "더코디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043090.KQ",
  "name": "더테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "213420.KQ",
  "name": "덕산네오룩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317330.KQ",
  "name": "덕산테코피아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "077360.KQ",
  "name": "덕산하이메탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090410.KQ",
  "name": "덕신이피씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263600.KQ",
  "name": "덕우전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "194480.KQ",
  "name": "데브시스터즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263800.KQ",
  "name": "데이타솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206560.KQ",
  "name": "덱스터",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "261200.KQ",
  "name": "덴티스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067990.KQ",
  "name": "도이치모터스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006620.KQ",
  "name": "동구바이오제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100130.KQ",
  "name": "동국S&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005160.KQ",
  "name": "동국산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "075970.KQ",
  "name": "동국알앤에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086450.KQ",
  "name": "동국제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099410.KQ",
  "name": "동방선기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033500.KQ",
  "name": "동성화인텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025950.KQ",
  "name": "동신건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088130.KQ",
  "name": "동아엘텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041930.KQ",
  "name": "동아화성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060380.KQ",
  "name": "동양에스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079960.KQ",
  "name": "동양이엔피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228340.KQ",
  "name": "동양파일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088910.KQ",
  "name": "동우팜투테이블",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094170.KQ",
  "name": "동운아나텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013120.KQ",
  "name": "동원개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109860.KQ",
  "name": "동일금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032960.KQ",
  "name": "동일기연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023790.KQ",
  "name": "동일철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005290.KQ",
  "name": "동진쎄미켐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025900.KQ",
  "name": "동화기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131970.KQ",
  "name": "두산테스나",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073190.KQ",
  "name": "듀오백",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030350.KQ",
  "name": "드래곤플라이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203650.KQ",
  "name": "드림시큐리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "223250.KQ",
  "name": "드림씨아이에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060570.KQ",
  "name": "드림어스컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "362990.KQ",
  "name": "드림인사이트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217620.KQ",
  "name": "디딤이앤에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016670.KQ",
  "name": "디모아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187870.KQ",
  "name": "디바이스이엔지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "110990.KQ",
  "name": "디아이티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263690.KQ",
  "name": "디알젬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214680.KQ",
  "name": "디알텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347850.KQ",
  "name": "디앤디파마텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263720.KQ",
  "name": "디앤씨미디어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376300.KQ",
  "name": "디어유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109740.KQ",
  "name": "디에스케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196490.KQ",
  "name": "디에이테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066900.KQ",
  "name": "디에이피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "127120.KQ",
  "name": "디엔에이링크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092070.KQ",
  "name": "디엔에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039840.KQ",
  "name": "디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "219550.KQ",
  "name": "디와이디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "310870.KQ",
  "name": "디와이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104460.KQ",
  "name": "디와이피엔에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079810.KQ",
  "name": "디이엔티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "113810.KQ",
  "name": "디젠스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043360.KQ",
  "name": "디지아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "197140.KQ",
  "name": "디지캡",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068930.KQ",
  "name": "디지털대성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033130.KQ",
  "name": "디지틀조선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "105740.KQ",
  "name": "디케이락",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263020.KQ",
  "name": "디케이앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290550.KQ",
  "name": "디케이티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066670.KQ",
  "name": "디티씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187220.KQ",
  "name": "디티앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "383930.KQ",
  "name": "디티앤씨알오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131180.KQ",
  "name": "딜리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "315640.KQ",
  "name": "딥노이드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "223310.KQ",
  "name": "딥마인드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317120.KQ",
  "name": "라닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042510.KQ",
  "name": "라온시큐어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "232680.KQ",
  "name": "라온테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418420.KQ",
  "name": "라온텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "300120.KQ",
  "name": "라온피플",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "171120.KQ",
  "name": "라이온켐텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "388790.KQ",
  "name": "라이콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347700.KQ",
  "name": "라이프시맨틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214260.KQ",
  "name": "라파스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200350.KQ",
  "name": "래몽래인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "171010.KQ",
  "name": "램테크놀러지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084650.KQ",
  "name": "랩지노믹스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217500.KQ",
  "name": "러셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038390.KQ",
  "name": "레드캡투어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "294140.KQ",
  "name": "레몬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "443250.KQ",
  "name": "레뷰코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228670.KQ",
  "name": "레이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228850.KQ",
  "name": "레이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "412350.KQ",
  "name": "레이저쎌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199550.KQ",
  "name": "레이저옵텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "281740.KQ",
  "name": "레이크머티리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "277810.KQ",
  "name": "레인보우로보틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215100.KQ",
  "name": "로보로보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090360.KQ",
  "name": "로보스타",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108490.KQ",
  "name": "로보티즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900260.KQ",
  "name": "로스웰",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067730.KQ",
  "name": "로지시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071280.KQ",
  "name": "로체시스템즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "328130.KQ",
  "name": "루닛",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038060.KQ",
  "name": "루멘스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060240.KQ",
  "name": "룽투코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "141080.KQ",
  "name": "리가켐바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058470.KQ",
  "name": "리노공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016100.KQ",
  "name": "리더스코스메틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012700.KQ",
  "name": "리드코프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "302550.KQ",
  "name": "리메드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073570.KQ",
  "name": "리튬포어스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377450.KQ",
  "name": "리파인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "277070.KQ",
  "name": "린드먼아시아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042500.KQ",
  "name": "링네트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "193250.KQ",
  "name": "링크드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "219420.KQ",
  "name": "링크제니시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439090.KQ",
  "name": "마녀공장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "195500.KQ",
  "name": "마니커에프앤지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377480.KQ",
  "name": "마음AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "305090.KQ",
  "name": "마이크로디지탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "098120.KQ",
  "name": "마이크로컨텍솔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424980.KQ",
  "name": "마이크로투나노",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038290.KQ",
  "name": "마크로젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "267980.KQ",
  "name": "매일유업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005990.KQ",
  "name": "매일홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093520.KQ",
  "name": "매커스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377030.KQ",
  "name": "맥스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100590.KQ",
  "name": "머큐리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067280.KQ",
  "name": "멀티캠퍼스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072870.KQ",
  "name": "메가스터디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215200.KQ",
  "name": "메가스터디교육",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "133750.KQ",
  "name": "메가엠디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446540.KQ",
  "name": "메가터치",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "235980.KQ",
  "name": "메드팩토",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041920.KQ",
  "name": "메디아나",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014100.KQ",
  "name": "메디앙스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054180.KQ",
  "name": "메디콕스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086900.KQ",
  "name": "메디톡스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078160.KQ",
  "name": "메디포스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "408920.KQ",
  "name": "메쎄이상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021880.KQ",
  "name": "메이슨캐피탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140410.KQ",
  "name": "메지온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241770.KQ",
  "name": "메카로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059210.KQ",
  "name": "메타바이오메드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058110.KQ",
  "name": "멕아이씨에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "434480.KQ",
  "name": "모니터랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080420.KQ",
  "name": "모다이노칩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417970.KQ",
  "name": "모델솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080160.KQ",
  "name": "모두투어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "087260.KQ",
  "name": "모바일어플라이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101330.KQ",
  "name": "모베이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012860.KQ",
  "name": "모베이스전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "363260.KQ",
  "name": "모비데이즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348030.KQ",
  "name": "모비릭스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "250060.KQ",
  "name": "모비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "288980.KQ",
  "name": "모아데이타",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "142760.KQ",
  "name": "모아라이프플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033200.KQ",
  "name": "모아텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "333050.KQ",
  "name": "모코엠시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "118990.KQ",
  "name": "모트렉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006920.KQ",
  "name": "모헨즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001810.KQ",
  "name": "무림SP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "279600.KQ",
  "name": "미디어젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095500.KQ",
  "name": "미래나노텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "254490.KQ",
  "name": "미래반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "218150.KQ",
  "name": "미래생명자원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442900.KQ",
  "name": "미래에셋드림스팩1호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100790.KQ",
  "name": "미래에셋벤처투자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "412930.KQ",
  "name": "미래에셋비전스팩1호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446190.KQ",
  "name": "미래에셋비전스팩2호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448830.KQ",
  "name": "미래에셋비전스팩3호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049950.KQ",
  "name": "미래컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "207760.KQ",
  "name": "미스터블루",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059090.KQ",
  "name": "미코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214610.KQ",
  "name": "미코바이오메드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "201490.KQ",
  "name": "미투온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452200.KQ",
  "name": "민테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418470.KQ",
  "name": "밀리의서재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206640.KQ",
  "name": "바디텍메드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018700.KQ",
  "name": "바른손",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035620.KQ",
  "name": "바른손이앤에이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053030.KQ",
  "name": "바이넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "301300.KQ",
  "name": "바이브컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064550.KQ",
  "name": "바이오니아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "314930.KQ",
  "name": "바이오다인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208710.KQ",
  "name": "바이오로그디바이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086820.KQ",
  "name": "바이오솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038460.KQ",
  "name": "바이오스마트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251120.KQ",
  "name": "바이오에프디엔씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199730.KQ",
  "name": "바이오인프라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086040.KQ",
  "name": "바이오톡스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099430.KQ",
  "name": "바이오플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032980.KQ",
  "name": "바이온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "308080.KQ",
  "name": "바이젠셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043150.KQ",
  "name": "바텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "323990.KQ",
  "name": "박셀바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "267790.KQ",
  "name": "배럴",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046310.KQ",
  "name": "백금T&A",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "331520.KQ",
  "name": "밸로프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "438700.KQ",
  "name": "버넥트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066410.KQ",
  "name": "버킷스튜디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "382900.KQ",
  "name": "범한퓨얼셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206400.KQ",
  "name": "베노티앤알",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019010.KQ",
  "name": "베뉴지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "177350.KQ",
  "name": "베셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424760.KQ",
  "name": "벨로크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225530.KQ",
  "name": "보광산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "250000.KQ",
  "name": "보라티알",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "310210.KQ",
  "name": "보로노이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006910.KQ",
  "name": "보성파워텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226340.KQ",
  "name": "본느",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014470.KQ",
  "name": "부방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008470.KQ",
  "name": "부스타",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "338220.KQ",
  "name": "뷰노",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100120.KQ",
  "name": "뷰웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "406820.KQ",
  "name": "뷰티스킨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "337930.KQ",
  "name": "브랜드엑스코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099390.KQ",
  "name": "브레인즈컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064480.KQ",
  "name": "브리지텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "288330.KQ",
  "name": "브릿지바이오테라퓨틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365900.KQ",
  "name": "브이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089970.KQ",
  "name": "브이엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251630.KQ",
  "name": "브이원텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018290.KQ",
  "name": "브이티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044480.KQ",
  "name": "블레이드 Ent",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439580.KQ",
  "name": "블루엠텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033560.KQ",
  "name": "블루콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "369370.KQ",
  "name": "블리츠웨이스튜디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126340.KQ",
  "name": "비나텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121800.KQ",
  "name": "비덴트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148140.KQ",
  "name": "비디아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082800.KQ",
  "name": "비보존 제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318410.KQ",
  "name": "비비씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419540.KQ",
  "name": "비스토스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "146320.KQ",
  "name": "비씨엔씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200780.KQ",
  "name": "비씨월드제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "413640.KQ",
  "name": "비아이매트릭스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "141000.KQ",
  "name": "비아트론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083650.KQ",
  "name": "비에이치아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445360.KQ",
  "name": "비엔케이제1호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "473370.KQ",
  "name": "비엔케이제2호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065170.KQ",
  "name": "비엘팜텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086670.KQ",
  "name": "비엠티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "335890.KQ",
  "name": "비올",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "230980.KQ",
  "name": "비유테크놀러지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138580.KQ",
  "name": "비즈니스온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082920.KQ",
  "name": "비츠로셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054220.KQ",
  "name": "비츠로시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042370.KQ",
  "name": "비츠로테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050090.KQ",
  "name": "비케이홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148780.KQ",
  "name": "비큐에이아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307870.KQ",
  "name": "비투엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357880.KQ",
  "name": "비트나인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032850.KQ",
  "name": "비트컴퓨터",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238200.KQ",
  "name": "비피도",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093190.KQ",
  "name": "빅솔론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065450.KQ",
  "name": "빅텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "210120.KQ",
  "name": "빅텐츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069540.KQ",
  "name": "빛과전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072950.KQ",
  "name": "빛샘전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451250.KQ",
  "name": "삐아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "143240.KQ",
  "name": "사람인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452430.KQ",
  "name": "사피엔반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419120.KQ",
  "name": "산돌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122350.KQ",
  "name": "삼기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419050.KQ",
  "name": "삼기이브이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014970.KQ",
  "name": "삼륭물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018310.KQ",
  "name": "삼목에스폼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053700.KQ",
  "name": "삼보모터스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009620.KQ",
  "name": "삼보산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023600.KQ",
  "name": "삼보판지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "425290.KQ",
  "name": "삼성스팩6호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439250.KQ",
  "name": "삼성스팩7호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448740.KQ",
  "name": "삼성스팩8호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "468510.KQ",
  "name": "삼성스팩9호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009300.KQ",
  "name": "삼아제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "361670.KQ",
  "name": "삼영에스앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054540.KQ",
  "name": "삼영엠텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065570.KQ",
  "name": "삼영이엔씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032280.KQ",
  "name": "삼일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "002290.KQ",
  "name": "삼일기업공사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037460.KQ",
  "name": "삼지전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032750.KQ",
  "name": "삼진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054090.KQ",
  "name": "삼진엘앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "000250.KQ",
  "name": "삼천당제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024950.KQ",
  "name": "삼천리자전거",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038500.KQ",
  "name": "삼표시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "437730.KQ",
  "name": "삼현",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017480.KQ",
  "name": "삼현철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046390.KQ",
  "name": "삼화네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027580.KQ",
  "name": "상보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038540.KQ",
  "name": "상상인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101000.KQ",
  "name": "상상인인더스트리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "415580.KQ",
  "name": "상상인제3호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452670.KQ",
  "name": "상상인제4호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091580.KQ",
  "name": "상신이디피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263810.KQ",
  "name": "상신전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089980.KQ",
  "name": "상아프론테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042940.KQ",
  "name": "상지건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042600.KQ",
  "name": "새로닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "107600.KQ",
  "name": "새빗켐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "411080.KQ",
  "name": "샌즈랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "252990.KQ",
  "name": "샘씨엔에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "378800.KQ",
  "name": "샤페론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "294630.KQ",
  "name": "서남",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038070.KQ",
  "name": "서린바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006730.KQ",
  "name": "서부T&D",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079650.KQ",
  "name": "서산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100660.KQ",
  "name": "서암기계공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019770.KQ",
  "name": "서연탑메탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043710.KQ",
  "name": "서울리거",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092190.KQ",
  "name": "서울바이오시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046890.KQ",
  "name": "서울반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063170.KQ",
  "name": "서울옥션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027040.KQ",
  "name": "서울전자통신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018680.KQ",
  "name": "서울제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093920.KQ",
  "name": "서원인텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189860.KQ",
  "name": "서전기전",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "178320.KQ",
  "name": "서진시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122690.KQ",
  "name": "서진오토모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140070.KQ",
  "name": "서플러스글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011370.KQ",
  "name": "서한",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065710.KQ",
  "name": "서호전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035890.KQ",
  "name": "서희건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357550.KQ",
  "name": "석경에이티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003100.KQ",
  "name": "선광",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067370.KQ",
  "name": "선바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "171090.KQ",
  "name": "선익시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086710.KQ",
  "name": "선진뷰티사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014620.KQ",
  "name": "성광벤드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037350.KQ",
  "name": "성도이엔지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "081580.KQ",
  "name": "성우전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045300.KQ",
  "name": "성우테크론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "015750.KQ",
  "name": "성우하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365340.KQ",
  "name": "성일하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080470.KQ",
  "name": "성창오토텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043260.KQ",
  "name": "성호전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148150.KQ",
  "name": "세경하이테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "188260.KQ",
  "name": "세니젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053060.KQ",
  "name": "세동",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340440.KQ",
  "name": "세림B&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017510.KQ",
  "name": "세명전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011560.KQ",
  "name": "세보엠이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "396300.KQ",
  "name": "세아메카닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100700.KQ",
  "name": "세운메디칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024830.KQ",
  "name": "세원물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "258830.KQ",
  "name": "세종메디칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036630.KQ",
  "name": "세종텔레콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039310.KQ",
  "name": "세중",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067770.KQ",
  "name": "세진티에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053450.KQ",
  "name": "세코닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222810.KQ",
  "name": "세토피아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "252500.KQ",
  "name": "세화피앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "321370.KQ",
  "name": "센서뷰",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347000.KQ",
  "name": "센코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "331920.KQ",
  "name": "셀레믹스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049180.KQ",
  "name": "셀루메드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299660.KQ",
  "name": "셀리드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "268600.KQ",
  "name": "셀리버리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108860.KQ",
  "name": "셀바스AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208370.KQ",
  "name": "셀바스헬스케어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318160.KQ",
  "name": "셀바이오휴먼텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068760.KQ",
  "name": "셀트리온제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068940.KQ",
  "name": "셀피글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060230.KQ",
  "name": "소니드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290690.KQ",
  "name": "소룩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950200.KQ",
  "name": "소마젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032680.KQ",
  "name": "소프트센",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032685.KQ",
  "name": "소프트센우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "258790.KQ",
  "name": "소프트캠프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066910.KQ",
  "name": "손오공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043100.KQ",
  "name": "솔고바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035610.KQ",
  "name": "솔본",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357780.KQ",
  "name": "솔브레인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036830.KQ",
  "name": "솔브레인홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "304100.KQ",
  "name": "솔트룩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "328380.KQ",
  "name": "솔트웨어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086980.KQ",
  "name": "쇼박스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050960.KQ",
  "name": "수산아이앤티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084180.KQ",
  "name": "수성웹툰",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "253840.KQ",
  "name": "수젠텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298830.KQ",
  "name": "슈어소프트테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "236200.KQ",
  "name": "슈프리마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094840.KQ",
  "name": "슈프리마에이치큐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "192440.KQ",
  "name": "슈피겐코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424960.KQ",
  "name": "스마트레이더시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136510.KQ",
  "name": "스마트솔루션즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099440.KQ",
  "name": "스맥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033790.KQ",
  "name": "스카이문스테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "276040.KQ",
  "name": "스코넥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "159910.KQ",
  "name": "스킨앤스킨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115570.KQ",
  "name": "스타플렉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "330730.KQ",
  "name": "스톤브릿지벤처스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352090.KQ",
  "name": "스톰테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "253450.KQ",
  "name": "스튜디오드래곤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "408900.KQ",
  "name": "스튜디오미르",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204630.KQ",
  "name": "스튜디오산타클로스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "415380.KQ",
  "name": "스튜디오삼익",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013810.KQ",
  "name": "스페코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203690.KQ",
  "name": "스피어파워",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049830.KQ",
  "name": "승일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "020710.KQ",
  "name": "시공테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033170.KQ",
  "name": "시그네틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048870.KQ",
  "name": "시너지이노베이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025320.KQ",
  "name": "시노펙스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "269620.KQ",
  "name": "시스웍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "429270.KQ",
  "name": "시지트로닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418250.KQ",
  "name": "시큐레터",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131090.KQ",
  "name": "시큐브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "232830.KQ",
  "name": "시큐센",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290520.KQ",
  "name": "신도기연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001000.KQ",
  "name": "신라섬유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025870.KQ",
  "name": "신라에스지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215600.KQ",
  "name": "신라젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065350.KQ",
  "name": "신성델타테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "416180.KQ",
  "name": "신성에스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "162300.KQ",
  "name": "신스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290560.KQ",
  "name": "신시웨이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "002800.KQ",
  "name": "신신제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "472220.KQ",
  "name": "신영스팩10호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "430220.KQ",
  "name": "신영스팩8호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445970.KQ",
  "name": "신영스팩9호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017000.KQ",
  "name": "신원종합개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012790.KQ",
  "name": "신일제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138070.KQ",
  "name": "신진에스엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226330.KQ",
  "name": "신테카바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418210.KQ",
  "name": "신한제10호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452980.KQ",
  "name": "신한제11호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "474660.KQ",
  "name": "신한제12호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "474930.KQ",
  "name": "신한제13호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "405640.KQ",
  "name": "신한제9호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056700.KQ",
  "name": "신화인터텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187270.KQ",
  "name": "신화콘텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "243840.KQ",
  "name": "신흥에스이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "257720.KQ",
  "name": "실리콘투",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222800.KQ",
  "name": "심텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036710.KQ",
  "name": "심텍홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "160980.KQ",
  "name": "싸이맥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "356890.KQ",
  "name": "싸이버원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217330.KQ",
  "name": "싸이토젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010280.KQ",
  "name": "쌍용정보통신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208640.KQ",
  "name": "썸에이지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222420.KQ",
  "name": "쎄노텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037760.KQ",
  "name": "쎄니트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099320.KQ",
  "name": "쎄트렉아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049960.KQ",
  "name": "쎌바이오텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088280.KQ",
  "name": "쏘닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050890.KQ",
  "name": "쏠리드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109670.KQ",
  "name": "씨싸이트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066790.KQ",
  "name": "씨씨에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222080.KQ",
  "name": "씨아이에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352480.KQ",
  "name": "씨앤씨인터내셔널",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "264660.KQ",
  "name": "씨앤지하이테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352700.KQ",
  "name": "씨앤투스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "297090.KQ",
  "name": "씨에스베어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900120.KQ",
  "name": "씨엑스아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "359090.KQ",
  "name": "씨엔알리서치",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115530.KQ",
  "name": "씨엔플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115480.KQ",
  "name": "씨유메디칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340810.KQ",
  "name": "씨유박스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376290.KQ",
  "name": "씨유테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189330.KQ",
  "name": "씨이랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096530.KQ",
  "name": "씨젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101240.KQ",
  "name": "씨큐브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060590.KQ",
  "name": "씨티씨바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "260930.KQ",
  "name": "씨티케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052300.KQ",
  "name": "씨티프라퍼티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013990.KQ",
  "name": "아가방컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123860.KQ",
  "name": "아나패스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025980.KQ",
  "name": "아난티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "125210.KQ",
  "name": "아모그린텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357580.KQ",
  "name": "아모센스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052710.KQ",
  "name": "아모텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "074430.KQ",
  "name": "아미노로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092040.KQ",
  "name": "아미코젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083930.KQ",
  "name": "아바코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "149950.KQ",
  "name": "아바텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036010.KQ",
  "name": "아비코전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050860.KQ",
  "name": "아세아텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136410.KQ",
  "name": "아셈스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246720.KQ",
  "name": "아스타",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067390.KQ",
  "name": "아스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "159010.KQ",
  "name": "아스플로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "127710.KQ",
  "name": "아시아경제",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "154030.KQ",
  "name": "아시아종묘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "227610.KQ",
  "name": "아우딘퓨쳐스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "143160.KQ",
  "name": "아이디스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054800.KQ",
  "name": "아이디스홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "332370.KQ",
  "name": "아이디피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "339950.KQ",
  "name": "아이비김영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099190.KQ",
  "name": "아이센스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "289010.KQ",
  "name": "아이스크림에듀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214430.KQ",
  "name": "아이쓰리시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040910.KQ",
  "name": "아이씨디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "368600.KQ",
  "name": "아이씨에이치",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052860.KQ",
  "name": "아이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069920.KQ",
  "name": "아이에스이커머스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038880.KQ",
  "name": "아이에이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307180.KQ",
  "name": "아이엘사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101390.KQ",
  "name": "아이엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "461030.KQ",
  "name": "아이엠비디엑스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451220.KQ",
  "name": "아이엠티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078860.KQ",
  "name": "아이오케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090150.KQ",
  "name": "아이윈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123010.KQ",
  "name": "아이윈플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031310.KQ",
  "name": "아이즈비전",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "185490.KQ",
  "name": "아이진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059100.KQ",
  "name": "아이컴포넌트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "262840.KQ",
  "name": "아이퀘스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "175250.KQ",
  "name": "아이큐어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052460.KQ",
  "name": "아이크래프트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "119830.KQ",
  "name": "아이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052770.KQ",
  "name": "아이톡시",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "124500.KQ",
  "name": "아이티센",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "372800.KQ",
  "name": "아이티아이즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084850.KQ",
  "name": "아이티엠반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114840.KQ",
  "name": "아이패밀리에스씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027360.KQ",
  "name": "아주IB투자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032080.KQ",
  "name": "아즈텍WB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013310.KQ",
  "name": "아진산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059120.KQ",
  "name": "아진엑스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "158430.KQ",
  "name": "아톤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "321820.KQ",
  "name": "아티스트유나이티드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001540.KQ",
  "name": "안국약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053800.KQ",
  "name": "안랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065660.KQ",
  "name": "안트로젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "297570.KQ",
  "name": "알로이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "260660.KQ",
  "name": "알리코제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "354320.KQ",
  "name": "알멕",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "361570.KQ",
  "name": "알비더블유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131370.KQ",
  "name": "알서포트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140670.KQ",
  "name": "알에스오토메이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096610.KQ",
  "name": "알에프세미",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "061040.KQ",
  "name": "알에프텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148250.KQ",
  "name": "알엔투테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347860.KQ",
  "name": "알체라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196170.KQ",
  "name": "알테오젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123750.KQ",
  "name": "알톤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085810.KQ",
  "name": "알티캐스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "117670.KQ",
  "name": "알파홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "314140.KQ",
  "name": "알피바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "291650.KQ",
  "name": "압타머사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "293780.KQ",
  "name": "압타바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196300.KQ",
  "name": "애니젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "310200.KQ",
  "name": "애니플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299910.KQ",
  "name": "애닉",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "179530.KQ",
  "name": "애드바이오텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900100.KQ",
  "name": "애머릿지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "205500.KQ",
  "name": "액션스퀘어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052790.KQ",
  "name": "액토즈소프트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290740.KQ",
  "name": "액트로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238090.KQ",
  "name": "앤디포스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092600.KQ",
  "name": "앤씨앤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "129890.KQ",
  "name": "앱코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "174900.KQ",
  "name": "앱클론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "255440.KQ",
  "name": "야스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030960.KQ",
  "name": "양지사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "102120.KQ",
  "name": "어보브반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263540.KQ",
  "name": "어스앤에어로스페이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238120.KQ",
  "name": "얼라인드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019990.KQ",
  "name": "에너토크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "270660.KQ",
  "name": "에브리봇",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038680.KQ",
  "name": "에스넷",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217480.KQ",
  "name": "에스디생명공학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121890.KQ",
  "name": "에스디시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "304360.KQ",
  "name": "에스바이오메딕스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389500.KQ",
  "name": "에스비비테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042110.KQ",
  "name": "에스씨디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298060.KQ",
  "name": "에스씨엠생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065420.KQ",
  "name": "에스아이리소스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "103230.KQ",
  "name": "에스앤더블류",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "260970.KQ",
  "name": "에스앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101490.KQ",
  "name": "에스앤에스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095910.KQ",
  "name": "에스에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "275630.KQ",
  "name": "에스에스알",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031330.KQ",
  "name": "에스에이엠티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060540.KQ",
  "name": "에스에이티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "351320.KQ",
  "name": "에스에이티이엔지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056190.KQ",
  "name": "에스에프에이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080000.KQ",
  "name": "에스엔유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214310.KQ",
  "name": "에스엘에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246250.KQ",
  "name": "에스엘에스바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041510.KQ",
  "name": "에스엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007820.KQ",
  "name": "에스엠코어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109610.KQ",
  "name": "에스와이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365330.KQ",
  "name": "에스와이스틸텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031860.KQ",
  "name": "에스유홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "306040.KQ",
  "name": "에스제이그룹",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457940.KQ",
  "name": "에스케이증권제10호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "472230.KQ",
  "name": "에스케이증권제11호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "473000.KQ",
  "name": "에스케이증권제12호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "435870.KQ",
  "name": "에스케이증권제8호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455910.KQ",
  "name": "에스케이증권제9호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096630.KQ",
  "name": "에스코넥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069510.KQ",
  "name": "에스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234300.KQ",
  "name": "에스트래픽",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039440.KQ",
  "name": "에스티아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "098660.KQ",
  "name": "에스티오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052020.KQ",
  "name": "에스티큐브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "237690.KQ",
  "name": "에스티팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050760.KQ",
  "name": "에스폴리텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "288620.KQ",
  "name": "에스퓨얼셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "443670.KQ",
  "name": "에스피소프트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317830.KQ",
  "name": "에스피시스템스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058610.KQ",
  "name": "에스피지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043340.KQ",
  "name": "에쎈테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187660.KQ",
  "name": "에이디엠코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054630.KQ",
  "name": "에이디칩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200710.KQ",
  "name": "에이디테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096690.KQ",
  "name": "에이루트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298380.KQ",
  "name": "에이비엘바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203400.KQ",
  "name": "에이비온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "195990.KQ",
  "name": "에이비프로바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003800.KQ",
  "name": "에이스침대",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088800.KQ",
  "name": "에이스테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241840.KQ",
  "name": "에이스토리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "453860.KQ",
  "name": "에이에스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "312610.KQ",
  "name": "에이에프더블류",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "172670.KQ",
  "name": "에이엘티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445090.KQ",
  "name": "에이직랜드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072990.KQ",
  "name": "에이치시티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "239610.KQ",
  "name": "에이치엘사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "462020.KQ",
  "name": "에이치엠씨제6호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148930.KQ",
  "name": "에이치와이티씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044780.KQ",
  "name": "에이치케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357230.KQ",
  "name": "에이치피오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "355690.KQ",
  "name": "에이텀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071670.KQ",
  "name": "에이테크솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045660.KQ",
  "name": "에이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "224110.KQ",
  "name": "에이텍모빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021080.KQ",
  "name": "에이티넘인베스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089530.KQ",
  "name": "에이티세미콘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200470.KQ",
  "name": "에이팩트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "262260.KQ",
  "name": "에이프로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "397030.KQ",
  "name": "에이프릴바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "230240.KQ",
  "name": "에치에프알",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "230360.KQ",
  "name": "에코마케팅",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038870.KQ",
  "name": "에코바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "097780.KQ",
  "name": "에코볼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448280.KQ",
  "name": "에코아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101360.KQ",
  "name": "에코앤드림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "128540.KQ",
  "name": "에코캡",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086520.KQ",
  "name": "에코프로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "247540.KQ",
  "name": "에코프로비엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "383310.KQ",
  "name": "에코프로에이치엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038110.KQ",
  "name": "에코플라스틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073540.KQ",
  "name": "에프알텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064850.KQ",
  "name": "에프앤가이드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036810.KQ",
  "name": "에프에스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "173940.KQ",
  "name": "에프엔씨엔터",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083500.KQ",
  "name": "에프엔에스테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054940.KQ",
  "name": "엑사이엔씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950130.KQ",
  "name": "엑세스바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "205100.KQ",
  "name": "엑셈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "356680.KQ",
  "name": "엑스게이트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "070300.KQ",
  "name": "엑스큐어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317770.KQ",
  "name": "엑스페릭스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "373200.KQ",
  "name": "엑스플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092870.KQ",
  "name": "엑시콘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317870.KQ",
  "name": "엔바이오니아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067570.KQ",
  "name": "엔브이에이치코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "236810.KQ",
  "name": "엔비티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "333620.KQ",
  "name": "엔시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101400.KQ",
  "name": "엔시트론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "391060.KQ",
  "name": "엔에이치스팩20호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "422040.KQ",
  "name": "엔에이치스팩23호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "437780.KQ",
  "name": "엔에이치스팩24호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "438580.KQ",
  "name": "엔에이치스팩25호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439410.KQ",
  "name": "엔에이치스팩26호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440820.KQ",
  "name": "엔에이치스팩27호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451700.KQ",
  "name": "엔에이치스팩29호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "466910.KQ",
  "name": "엔에이치스팩30호",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "265740.KQ",
  "name": "엔에프씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "354200.KQ",
  "name": "엔젠바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455900.KQ",
  "name": "엔젤로보틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419080.KQ",
  "name": "엔젯",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208860.KQ",
  "name": "엔지스테크널러지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "183490.KQ",
  "name": "엔지켐생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "182400.KQ",
  "name": "엔케이맥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348370.KQ",
  "name": "엔켐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058450.KQ",
  "name": "엔터파트너즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069410.KQ",
  "name": "엔텔스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "227950.KQ",
  "name": "엔투텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "291230.KQ",
  "name": "엔피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "198080.KQ",
  "name": "엔피디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048830.KQ",
  "name": "엔피케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096870.KQ",
  "name": "엘디티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290650.KQ",
  "name": "엘앤씨바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "156100.KQ",
  "name": "엘앤케이바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073110.KQ",
  "name": "엘엠에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083310.KQ",
  "name": "엘오티베큠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037950.KQ",
  "name": "엘컴텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "170920.KQ",
  "name": "엘티씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058630.KQ",
  "name": "엠게임",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058970.KQ",
  "name": "엠로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019590.KQ",
  "name": "엠벤처투자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "169330.KQ",
  "name": "엠브레인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "373170.KQ",
  "name": "엠아이큐브솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "179290.KQ",
  "name": "엠아이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009780.KQ",
  "name": "엠에스씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123040.KQ",
  "name": "엠에스오토텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "323230.KQ",
  "name": "엠에프엠코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032790.KQ",
  "name": "엠젠솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033160.KQ",
  "name": "엠케이전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347890.KQ",
  "name": "엠투아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033310.KQ",
  "name": "엠투엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "259630.KQ",
  "name": "엠플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060850.KQ",
  "name": "영림원소프트랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "143540.KQ",
  "name": "영우디에스피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036560.KQ",
  "name": "영풍정밀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "265560.KQ",
  "name": "영화테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036000.KQ",
  "name": "예림당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "250930.KQ",
  "name": "예선테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053280.KQ",
  "name": "예스24",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122640.KQ",
  "name": "예스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900300.KQ",
  "name": "오가닉티코스메틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045060.KQ",
  "name": "오공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080520.KQ",
  "name": "오디텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039830.KQ",
  "name": "오로라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "322310.KQ",
  "name": "오로스테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046120.KQ",
  "name": "오르비텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014940.KQ",
  "name": "오리엔탈정공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065500.KQ",
  "name": "오리엔트정공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010470.KQ",
  "name": "오리콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417860.KQ",
  "name": "오브젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352910.KQ",
  "name": "오비고",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053980.KQ",
  "name": "오상자이엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036220.KQ",
  "name": "오상헬스케어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052420.KQ",
  "name": "오성첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039200.KQ",
  "name": "오스코텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226400.KQ",
  "name": "오스테오닉",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031510.KQ",
  "name": "오스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "368970.KQ",
  "name": "오에스피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138080.KQ",
  "name": "오이솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080580.KQ",
  "name": "오킨스전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067170.KQ",
  "name": "오텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "353590.KQ",
  "name": "오토앤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "173130.KQ",
  "name": "오파스넷",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440320.KQ",
  "name": "오픈놀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049480.KQ",
  "name": "오픈베이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "394280.KQ",
  "name": "오픈엣지테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "309930.KQ",
  "name": "오하임앤컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "244460.KQ",
  "name": "올리패스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226950.KQ",
  "name": "올릭스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "057540.KQ",
  "name": "옴니시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131030.KQ",
  "name": "옵투스제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082210.KQ",
  "name": "옵트론텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109080.KQ",
  "name": "옵티시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "380540.KQ",
  "name": "옵티코어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "153710.KQ",
  "name": "옵티팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "432430.KQ",
  "name": "와이랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "338840.KQ",
  "name": "와이바이오로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122990.KQ",
  "name": "와이솔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "232140.KQ",
  "name": "와이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "112290.KQ",
  "name": "와이씨켐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065530.KQ",
  "name": "와이어블",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067900.KQ",
  "name": "와이엔텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007530.KQ",
  "name": "와이엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "155650.KQ",
  "name": "와이엠씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "273640.KQ",
  "name": "와이엠텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251370.KQ",
  "name": "와이엠티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066430.KQ",
  "name": "와이오엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "273060.KQ",
  "name": "와이즈버즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019210.KQ",
  "name": "와이지-원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122870.KQ",
  "name": "와이지엔터테인먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "332570.KQ",
  "name": "와이팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079000.KQ",
  "name": "와토스코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "403490.KQ",
  "name": "우듬지팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032820.KQ",
  "name": "우리기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041190.KQ",
  "name": "우리기술투자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115440.KQ",
  "name": "우리넷",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046970.KQ",
  "name": "우리로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082850.KQ",
  "name": "우리바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215360.KQ",
  "name": "우리산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072470.KQ",
  "name": "우리산업홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073560.KQ",
  "name": "우리손에프앤지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037400.KQ",
  "name": "우리엔터프라이즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "153490.KQ",
  "name": "우리이앤엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101170.KQ",
  "name": "우림피티에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066590.KQ",
  "name": "우수AMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "103840.KQ",
  "name": "우양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046940.KQ",
  "name": "우원개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215380.KQ",
  "name": "우정바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065680.KQ",
  "name": "우주일렉트로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018620.KQ",
  "name": "우진비앤지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457550.KQ",
  "name": "우진엔텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "396470.KQ",
  "name": "워트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307280.KQ",
  "name": "원바이오젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032940.KQ",
  "name": "원익",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "240810.KQ",
  "name": "원익IPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "074600.KQ",
  "name": "원익QnC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104830.KQ",
  "name": "원익머트리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014190.KQ",
  "name": "원익큐브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217820.KQ",
  "name": "원익피앤이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030530.KQ",
  "name": "원익홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012620.KQ",
  "name": "원일특강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "382840.KQ",
  "name": "원준",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "336570.KQ",
  "name": "원텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376980.KQ",
  "name": "원티드랩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008370.KQ",
  "name": "원풍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008290.KQ",
  "name": "원풍물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101160.KQ",
  "name": "월덱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064090.KQ",
  "name": "웨스트라이즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "336060.KQ",
  "name": "웨이버스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095270.KQ",
  "name": "웨이브일렉트로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065950.KQ",
  "name": "웰크론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "076080.KQ",
  "name": "웰크론한텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043590.KQ",
  "name": "웰킵스하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196700.KQ",
  "name": "웹스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069080.KQ",
  "name": "웹젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053580.KQ",
  "name": "웹케시",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071460.KQ",
  "name": "위니아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377460.KQ",
  "name": "위니아에이드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044340.KQ",
  "name": "위닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "330350.KQ",
  "name": "위더스제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348350.KQ",
  "name": "위드텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "112040.KQ",
  "name": "위메이드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101730.KQ",
  "name": "위메이드맥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123420.KQ",
  "name": "위메이드플레이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065370.KQ",
  "name": "위세아이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038620.KQ",
  "name": "위즈코프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299900.KQ",
  "name": "위지윅스튜디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036090.KQ",
  "name": "위지트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136540.KQ",
  "name": "윈스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "320000.KQ",
  "name": "윈텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "097800.KQ",
  "name": "윈팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "192390.KQ",
  "name": "윈하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "313760.KQ",
  "name": "윌링스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "335870.KQ",
  "name": "윙스풋",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900340.KQ",
  "name": "윙입푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036200.KQ",
  "name": "유니셈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018000.KQ",
  "name": "유니슨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203450.KQ",
  "name": "유니온커뮤니티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011320.KQ",
  "name": "유니크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086390.KQ",
  "name": "유니테스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241690.KQ",
  "name": "유니테크노",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "142210.KQ",
  "name": "유니트론텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048430.KQ",
  "name": "유라테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206650.KQ",
  "name": "유바이오로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089850.KQ",
  "name": "유비벨록스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084440.KQ",
  "name": "유비온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032620.KQ",
  "name": "유비케어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "264450.KQ",
  "name": "유비쿼스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078070.KQ",
  "name": "유비쿼스홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024800.KQ",
  "name": "유성티엔에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054930.KQ",
  "name": "유신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069330.KQ",
  "name": "유아이디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049520.KQ",
  "name": "유아이엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "435380.KQ",
  "name": "유안타제10호스팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "444920.KQ",
  "name": "유안타제11호스팩",
 },
 {
 },
]
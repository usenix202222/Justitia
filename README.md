# Justitia

## Introduction
![Workflow of DepImpact](architecture.png)
The Pandemic has fundamentally shaped many aspects ofour lives. One significant example is the ever-growing digi-tal transformation for virtually every type of business, suchas online courses, online conferencing, online medical andpharmaceutical systems, remote work forces, and so on.
Similarly, the legal sector is experiencing online transformation. To enable profound digital
transformation of legal contract, Justitia is the first system that synthesizes blockchain-executable
smart contracts that honor the semantics of legally binding agreements.

## Requirements
<ol>
<li>Python 3.7</li>
<li>Javascript</li>
</ol>

## Input
Legal contract

##Output
Smart contract which reflects the semantic requirements

##Setup
1. download and unzip [roberta-classification.zip](https://drive.google.com/file/d/1s8vbKgDeQ8NN4IpS3oPX87BJgWMJY1-w/view?usp=sharing), and assign the path to the variable CLASSIFIER_PATH.
2. unzip trained-qa.zip, and assign the path to the variable TRAINED_QA_MODEL_PATH
3. install the required packages and StanfordCorenlp pipeline
## How to run
First, users should generate the smartIR. To generate smartIR, users should execute
pipline_for_contract with two input parameters: legal contract location and output location.
After this execution, the res folder contains the four types progammable clauses and smartIR.


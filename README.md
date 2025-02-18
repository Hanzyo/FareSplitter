# FareSplitter
## To run:
Clone the repo and `cd FareSplitter/` \
`python3 src/simple.py -h` \
The format of the input file is the following \
For every bill/transaction made: 
- 1st to (N-1)th line: tax information. Space separate the tax name with its percent value (e.g. E 0.0 or A 9.25)
- Nth : total after tax price of the receipt (e.g. 128.5)
- (N+1)th to (M-1)th line: individual items that is not shared with others with its tax label. (e.g. Y 5.5 A) \
    Note: if a person does not have any individual item, please include them as well (e.g. M 0 E)
- Mth line: the person that paid for the transaction (e.g. Y)

End of transaction 1. Follow the same format for more transactions

See example input in `example_input`
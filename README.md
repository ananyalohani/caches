# CSE112: Computer Organisation 
## End Semester Assignment: Cache

__Name:__ Ananya Lohani
__Roll Number:__ 2019018
__Section:__ A
__Group:__ 9

#### Overview 
* Programming Language: Python 3.7
* Word Size: 16-bit
* Implemented a single level cache and a main memory containing 2^16 memory locations/addresses.
* All replacement schemes used are random replacement schemes. 

#### User Input
* Size of Cache in bytes(_S_)
* Number of Cache Lines(_CL_)
* Size of a Block in bytes(_B_)
* Number of ways(_N_) for N-way Set Associative Mapping
* Choice of mapping of cache

#### Types of Mapping of Cache
1. Direct Mapping
2. Fully Associative Mapping
3. N-way Set Associative Mapping

#### Operations
After taking the above inputs, the user will be prompted repeatedly to perform any of the following operations:
1. __Read:__ To read data from the address input by the user.
2. __Write:__ Address and data are input by the user. The data is stored at the specified location.
3. __View Cache:__ To display the state of the Cache, i.e. the block number occupying each cache line, and the data present in the blocks.
4. __View Sets:__ (Only applicable for N-way Set Associative Cache) To display the state of the Sets, i.e. the cache line(s) occupying each set.


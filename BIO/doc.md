## Q1 : Implement String Sort
#### Solution : 
* The approach opted to tackle the problem is to use two **Arrays of Link Lists** each of size **27**.<br>
* Say, length of the longest string is **L**. Hence, we will pad the rest of the strings with length less than **L** with **'$'** (smallest ascii value, let's say). <br>
* Now iteratively, we will be considering one character at a time of each string from the end and storing the strings in the DSs alternately, according to the charachters.<br>
* We will stop after the strings will be arranged on the basis of their first charachter.
#### Input Demo :
7 (No. of strings)<br>
abb<br>
Abd<br>
sd<br>
Sdffgr<br>
erew<br>
w<br>
er
#### Output Demo :
abb<br>
Abd<br>
er<br>
erew<br>
sd<br>
Sdffgr<br>
w
#### Time Complexity :
**L** : length of longest string<br>
**N** : No. of strings<br>
**Time Complexity** : O(NL)
#### Space Complexity :
**L** : length of longest string<br>
**N** : No. of strings<br>
**Space Complexity** : O(NL)

## Q2 : Given a string find the consecutive triples that have occurred most number of times
#### Solution :
* We are using **Trie** Data Structure to store all the triplets (consisting of 'a', 'g', 't', and 'c').
* During this process, every time we reach to depth three of any triplet, we increase the counter corresponding to that branch.
* Finally, we return the triplet(s) with the highest counter value.
#### Input Demo :
accaacctaccgggggaccggg (Given String)
#### Output Demo :
acc<br>
ggg<br>
(Both have frequency of 3)
#### Time Complexity:
**N** : Length of given string<br>
**Time Complexity** : O(N)
#### Space Complexity :
As, there can be at most 64 different triplets. So, maximum space required is in the order of (3x64).<br>
So, Space Complexity is **constant**.

## Q3 : Given three strings, Determine their longest common substring
#### Solution :
* Firstly, we have extracted all the suffixes of all the three strings and sorted them.
* Then, we traverse over the suffix array and find all the ranges **i..j** where there is at least one suffix from each given string, and find out the **longest common prefix** of the first and last suffix in that range.
* The pefix having the maximum length is our solution.
#### Input Demo :
abababccabbba<br>
aababcabbba<br>
aaababcaabbba<br>
#### Output Demo :
ababc<br>
abbba
(Both are length 5)
#### Time Complexity:
**N1** : Length of 1st string<br>
**N2** : Length of 2nd string<br>
**N3** : Length of 3rd string<br>
**N** : N1 + N2 + N3<br>
**M** : MAX(N1, N2, N3)<br>
**Time Complexity** : O(NlogN + MN)
#### Space Complexity :
O(MN) (To store all the strings)

## Nirbhay Sharma (B19CSE114)
## Blockchain Assignment - 1

---

### How To Run

**First create the conda env**

```
conda env create -n env_name -f env.yml
```

**Then activate the env**

```
conda activate env_name
```

**Then run the file**

```
python b19cse114.py
```

### How to Interpret

The program offers the following choices

- 0 for doing transaction
- 1 for printing blockchain
- 2 for printing utxo for specific user
- 3 for printing utxo for specific miner
- 4 for exiting

<strong class='bold_class'>First Choice (0)</strong>

<strong class='bold_class'>Input</strong>

- After Entering 0, please enter number of transactions you want to perform
- then enter the transaction in the format
- ```from_idx to_idx btc fees```
    - from_idx is the index of user from which the transaction is conducted
    - to_idx is the index of the user to which the btc is transferred
    - btc is the number of bitcoins transferred
    - fees is the transaction fees paid by the user to the miner

<strong class='bold_class'>Output</strong>

- It prints the miner selected for creating the block along with the hash of the block

<strong class='bold_class'>Second Choice (1)</strong>

<strong class='bold_class'>Input</strong>

- No Input is required

<strong class='bold_class'>Output</strong>

- It prints the entire blockchain
    - It prints header and body of the blockchain, header contains block_no, merkle_root_hash, timestamp, nonce etc and tail contains hash of transactions

<strong class='bold_class'>Third Choice (2)</strong>

<strong class='bold_class'>Input</strong>

- enter the user index for which you want to see utxo

<strong class='bold_class'>Output</strong>

- It prints the utxo for that particular user 

<strong class='bold_class'>Fourth Choice (3)</strong>

<strong class='bold_class'>Input</strong>

- enter the miner index for which you want to see utxo

<strong class='bold_class'>Output</strong>

- It prints the utxo for that particular miner

<strong class='bold_class'>Fifth choice (4)</strong>

- It breaks the loop and program is exited


### Sample Test Cases to Try for choice 1

```
# transactions

0 1 4 2
1 4 3 1
1 2 3 1
2 1 2 3

3 4 3 1
4 6 4 2

1 4 1 1
6 1 3 2
1 7 6 1

0 1 4 2
0 2 5 1
0 3 1 1

0 5 2 2
0 6 2 1
0 2 0.5 0.5

1 2 3 1
1 3 2 1
1 4 1 2
```

<style> 

table, th, td {
  border: 0.1px solid black;
  border-collapse: collapse;
}

* {
    font-family:"Monaco";
}

h3 {
  color: #e71989;
}

.bold_class {
    color:purple;
}

</style>

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">
    MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });
</script>
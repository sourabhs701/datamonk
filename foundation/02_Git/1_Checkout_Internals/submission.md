
**Secret.txt Blob**
```bash
git hash-object docs/secret.txt
git cat-file -p <hash>
```
![Secret Blob Output](./screenshot/ss0.png)

## Create a Tree (Commit)
```bash
git commit -m "Initial commit"
git log --oneline
```
![Initial Commit Log](./screenshot/ss1.png)

## Commit Internals
```bash
git cat-file -p <commit_hash>
```
![Commit Internals](./screenshot/ss2.png)

## Inspect the Tree
```bash
git cat-file -p <tree_hash>
```
![Tree Internals](./screenshot/ss3.png)

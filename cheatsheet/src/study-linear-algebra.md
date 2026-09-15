---
title: Study Reference — Linear Algebra
profile: study
---

# Linear Algebra — Study Reference

*Topics 1 & 2 · BSE Brush-Up 2026 · companion to the exam sheet*

This is the "why" document. Read it to build intuition; use the exam sheet to look things up under time pressure. Every worked example is taken from your lecture notes or problem sets.

**Contents**
1. Sets & functions
2. Vectors and vector spaces
3. Subspaces
4. Linear independence
5. Span, basis, dimension
6. Inner products, norms, distances, angles
7. Projections
8. Linear mappings, kernel and image
9. Matrix operations
10. Inverse, trace, determinant, rank, orthogonal matrices
11. Eigenvalues and eigenvectors
12. Definiteness
13. Decompositions

---

## 1. Sets & Functions

### Why this is here

Everything downstream is a set with structure bolted on. A vector space is a set plus two operations. A subspace is a subset that survives those operations. A linear map is a function between two such sets. Getting the vocabulary straight now saves confusion later.

### Sets

A **set** is a collection of distinct objects. Two ways to define one:

- **Listing:** $A=\{2,4,6,8\}$
- **Condition:** $B=\{x: x\in\mathbb{R},\ x^2<4\}$

The operations are the familiar ones, and the only two worth memorising are De Morgan's:

$$(A\cup B)^c=A^c\cap B^c \qquad (A\cap B)^c=A^c\cup B^c$$

*Negating an "or" gives an "and", and vice versa.* If you've ever debugged a `WHERE NOT (a OR b)` clause, you've used this.

The **power set** $2^A$ is the set of all subsets, including $\varnothing$ and $A$ itself. The notation is a hint: if $A$ has $n$ elements, $2^A$ has $2^n$ — each element is independently in or out.

### Functions

$f:A\to B$ assigns to **each** $a\in A$ **exactly one** $f(a)\in B$. $A$ is the **domain**, $B$ the **codomain**.

Two operations that look symmetric but aren't:

- **Image** $f(S)=\{f(s):s\in S\}$ — push a set forwards
- **Preimage** $f^{-1}(T)=\{a\in A: f(a)\in T\}$ — pull a set backwards

> The notation $f^{-1}(T)$ is defined **even when $f$ has no inverse function**. It's asking "which inputs land in $T$?", which always has an answer (possibly $\varnothing$). Don't read it as "apply the inverse".

### Injective, surjective, bijective

| | Definition | Plain English |
|---|---|---|
| **Injective** (one-to-one) | $f(a_1)=f(a_2)\Rightarrow a_1=a_2$ | no two inputs collide — **lossless** |
| **Surjective** (onto) | $f(A)=B$ | every target is hit — **complete coverage** |
| **Bijective** | both | perfect pairing |

An inverse function $f^{-1}:B\to A$ exists **if and only if** $f$ is bijective, and it's then unique.

Why both conditions? If $f$ isn't injective, two inputs share an output and $f^{-1}$ wouldn't know which to return. If $f$ isn't surjective, some $b\in B$ has no preimage and $f^{-1}(b)$ would be undefined. You need "exactly one" in both directions.

These three words come back in §8 as the central question about linear maps — and there, unlike for general functions, there's a cheap test.

---

## 2. Vectors and Vector Spaces

### What a vector actually is

Forget arrows for a moment. A vector space is a **set with a closure guarantee**.

Think of a type: "NumPy array of shape `(3,)`, dtype `float64`". The claim is that adding two of them, or scaling one, **always** gives you back something of the same type. Never a shape mismatch, never a string, never an error. That guarantee is called **closure**, and it's the whole idea.

Formally, $V=(\mathcal V,+,\cdot)$ — a set plus two operations:

$$+:\mathcal V\times\mathcal V\to\mathcal V \quad\text{(inner operation)} \qquad \cdot:\mathbb{R}\times\mathcal V\to\mathcal V \quad\text{(outer operation)}$$

Read those as type signatures. The `-> V` on the end is the closure guarantee.

$\mathcal V$ must contain the **neutral element** $\mathbf 0$, with $u+\mathbf 0=\mathbf 0+u=u$ for all $u$.

### The eight axioms, grouped

Don't memorise them as a list. They split into two groups:

**Group A — addition behaves like a well-mannered `SUM()`**

1. Associative: $(x+y)+z=x+(y+z)$
2. Commutative: $x+y=y+x$
3. Neutral element $\mathbf 0$
4. Every $x$ has an inverse $-x$

(Formally: $(\mathcal V,+)$ is an abelian group.)

**Group B — scalars interact sanely**

5. $\lambda(x+y)=\lambda x+\lambda y$
6. $(\lambda+\psi)x=\lambda x+\psi x$
7. $\lambda(\psi x)=(\lambda\psi)x$
8. $1\cdot x=x$

Axioms 5–7 are exactly why a compiler or a numerical library is free to rewrite `2*(u+v)` as `2*u + 2*v`, or to fuse loops, without changing the answer.

### Why axiomatise at all?

Because $\mathbb{R}^n$ isn't the only vector space. The set of all $m\times n$ matrices is one. Polynomials of degree $\le3$ are one. Functions $\mathbb{R}\to\mathbb{R}$ are one. Every theorem you prove about abstract vector spaces transfers to all of them **for free**.

It's an interface, and everything implementing it inherits the default methods.

### Columns, rows, transpose

$$c=\begin{bmatrix}x_1\\\vdots\\x_n\end{bmatrix}\in\mathbb{R}^{n\times1} \qquad r=\begin{bmatrix}x_1&\cdots&x_n\end{bmatrix}\in\mathbb{R}^{1\times n} \qquad c^\top=r,\quad r^\top=c$$

**Vectors are columns by default.** When you see $(1,2,3)^\top$ written inline, the transpose is there to tell you it's a column.

Concrete arithmetic:

$$a=\begin{bmatrix}2\\1\end{bmatrix},\ b=\begin{bmatrix}-0.5\\1\end{bmatrix} \Rightarrow a+b=\begin{bmatrix}1.5\\2\end{bmatrix},\qquad -2b=\begin{bmatrix}1\\-2\end{bmatrix}$$

### In data science

A vector is a finite-dimensional numerical array holding **features** (age, height), **parameters/weights**, **random variables**, or **derivatives**. A matrix is usually a data table: **rows = observations, columns = features**.

That last point deserves emphasis because it cuts against instinct. You naturally read a table row-wise, one record at a time. Most of linear algebra reads it **column-wise** — each feature, across all observations, treated as a single vector.

---

## 3. Subspaces

### The idea

A subspace is a **filtered view of a vector space that is still closed under the operations**.

The SQL framing is exact. Most `WHERE` clauses destroy closure; very few preserve it.

```sql
-- a subspace: the plane z = 0
SELECT * FROM vectors WHERE z = 0;
-- add two rows -> z is still 0. scale one -> still 0. closed.

-- NOT a subspace: the unit sphere
SELECT * FROM vectors WHERE x*x + y*y + z*z = 1;
-- add two rows -> length is no longer 1. you've fallen out of the view.
```

### The test

$U\subseteq V$ is a subspace if:

1. $U\neq\varnothing$, and $\mathbf 0\in U$
2. Closed under addition: $u,v\in U\Rightarrow u+v\in U$
3. Closed under scalar multiplication: $\lambda u\in U$ for all $\lambda\in\mathbb{R}$

Check (1) first — it's a single substitution and it kills most candidates immediately.

### The three examples from your notes

$V=\mathbb{R}^2$:

**$A=\{(x,x):x\in\mathbb{R}\}$** — the diagonal line through the origin.
Contains $\mathbf 0$ ✓. Sum of two points on the line is on the line ✓. Scaling stays on the line ✓. **Subspace.**

**$B=\{(x,x+1):x\in\mathbb{R}\}$** — the same line shifted up by 1.
Is $\mathbf 0$ on it? That needs $0=0+1$. No. **Not a subspace** — and you knew after one line of work.

**$C=\{(x,x):x\in\mathbb{R},\ x\ge0\}$** — the half-line.
Contains $\mathbf 0$ ✓. Closed under addition (two non-negatives sum to a non-negative) ✓. Closed under scaling? Take $\lambda=-1$: $(1,1)\mapsto(-1,-1)$, which has $x<0$. ✗ **Not a subspace.**

> $C$ is the instructive one. It passes two of three tests. **Always test scalar closure with a negative $\lambda$** — that's where half-spaces, rays, and "non-negative" constraints fail.

### The origin rule, and why it matters practically

**Every subspace contains the origin.** A line or plane that misses $\mathbf 0$ is called **affine**, not a subspace.

This is the reason behind a line of code you've probably typed without thinking:

```python
X_centered = X - X.mean(axis=0)
```

PCA finds the best-fitting **subspace**, and subspaces are anchored at the origin. If your data cloud sits at $(50,200)$, the best subspace through the origin points at the cloud's **location**, not its **shape** — your first principal component just recovers the mean vector and tells you nothing. Centring translates the affine set you care about into a genuine subspace.

### Union, intersection, sum

| | Subspace? |
|---|---|
| $U\cap W$ | ✅ always |
| $U\cup W$ | ❌ generally not |
| $U+W=\{u+w\}$ | ✅ always |

**Why the intersection works.** If $u$ and $w$ each satisfy *both* membership conditions, so does $u+w$. There's nothing to escape into.

**Why the union fails.** Take $U$ = x-axis, $W$ = y-axis in $\mathbb{R}^2$. Both are genuine subspaces. Now:

$$u=\begin{bmatrix}1\\0\end{bmatrix}\in U, \qquad w=\begin{bmatrix}0\\1\end{bmatrix}\in W, \qquad u+w=\begin{bmatrix}1\\1\end{bmatrix}$$

Is $(1,1)$ on the x-axis? No. On the y-axis? No. **Not in the union.** Additive closure is violated.

```
   y
 2 │  ·   ·   █   ·   ·        █ = in U ∪ W
 1 │  ·   ·   w━━━?   ·        ? = (1,1) — NOT in the union
   │          ┃   ┃
 0 │  █   █   O━━━u   █        The union is a plus sign: two solid
-1 │  ·   ·   █   ·   ·        arms and four empty quadrants.
   └────────────────────→ x
     -2  -1   0   1   2
```

The intuition: a union is an **OR**. It hands you the points of both pieces but **nothing in the gap between them**. Addition lets you walk along one arm then the other, landing straight in the empty quadrant.

In SQL terms: `UNION` is a set operation, not an algebraic one. Two tables that each respect an invariant internally give you a union that respects nothing.

**The exact condition:** $U\cup W$ is a subspace **iff** $U\subseteq W$ or $W\subseteq U$ — one nested inside the other, in which case the union is just the bigger one and nothing interesting happened.

**The fix** is the **sum** $U+W=\{u+w: u\in U, w\in W\}$, which is always a subspace and equals $\text{span}(U\cup W)$. For the two axes, $U+W=\mathbb{R}^2$ — the whole plane, not just the plus sign. In SQL terms you want a cross join and an addition, not a union.

If additionally $U\cap W=\{\mathbf 0\}$, it's a **direct sum** $U\oplus W$, and every vector decomposes **uniquely** into a $U$-part and a $W$-part. That uniqueness is what makes projections well-defined.

---

## 4. Linear Independence

### What it means

**Each vector must contribute a genuinely new direction.**

- **Independent** → every vector points somewhere the others can't reach
- **Dependent** → at least one is redundant; you could already get there without it

### The definition, and why it's phrased that way

$$\sum_{i=1}^k\lambda_ix_i=\mathbf 0 \ \Longrightarrow\ \lambda_1=\cdots=\lambda_k=0$$

You can always hit $\mathbf 0$ trivially by setting every $\lambda_i=0$. That tells you nothing. The question is whether there's **any other way**. If yes, the vectors are **dependent**.

What you *really* mean by dependent is "one of these is redundant". But which one? For

$$1v_1+1v_2-1v_3=\mathbf 0$$

you could equally say $v_3=v_1+v_2$, or $v_1=v_3-v_2$, or $v_2=v_3-v_1$. All true. The $\sum\lambda_ix_i=\mathbf 0$ form states that redundancy exists **without having to nominate a culprit**, and it needs no division. That's why it's the official definition.

### The geometry

```
 TWO VECTORS                    THREE IN R³
 INDEPENDENT      DEPENDENT     independent = enclose real volume
     ↑ v₂            ↗ v₂       dependent   = all lie in one plane
     │  ↗ v₁       ↗                         (volume = 0 → det = 0)
     │╱          ↗ v₁
     O────→     O
 different lines  same line
```

Independence means the vectors span as much space as their number allows. Dependence means they've collapsed into something lower-dimensional.

### The test

**Vectors as columns → row reduce to REF → independent iff every column has a pivot.**

A **pivot** is the first non-zero entry in a row. **REF** means only zeros appear below each leading entry.

From your notes, with $x_1=(1,2,-3,4)^\top$, $x_2=(1,1,0,2)^\top$, $x_3=(-1,-2,1,1)^\top$:

$$\begin{bmatrix}1&1&-1\\2&1&-2\\-3&0&1\\4&2&1\end{bmatrix} \xrightarrow[\substack{R_3+3R_1\\R_4-4R_1}]{R_2-2R_1} \begin{bmatrix}1&1&-1\\0&-1&0\\0&3&-2\\0&-2&5\end{bmatrix} \xrightarrow[\substack{R_3-3R_2\\R_4+2R_2}]{-R_2} \begin{bmatrix}\mathbf 1&1&-1\\0&\mathbf 1&0\\0&0&\mathbf{-2}\\0&0&5\end{bmatrix} \to \begin{bmatrix}\mathbf 1&1&-1\\0&\mathbf 1&0\\0&0&\mathbf{-2}\\0&0&0\end{bmatrix}$$

Three pivots for three columns → **independent**.

### Why row reduction is allowed to answer this

Every row operation is left-multiplication by an **invertible** elementary matrix, so the reduced matrix is $R=MA$ with $M$ invertible. Therefore

$$Ax=\mathbf 0 \iff MAx=\mathbf 0 \iff Rx=\mathbf 0$$

Not approximately — **exactly**. The same $x$ values solve both. So the columns of $R$ have precisely the same dependency relations as the columns of $A$.

**Row reduction is a dependency detector.** It re-expresses the same relationships in coordinates simple enough to read off by eye.

| Preserved by row operations? | |
|---|---|
| Kernel, column dependency relations, rank, row space | ✅ |
| **Column space (image)** | ❌ **changes** |

That ❌ is exactly why, when you want a basis for the image, you take the pivot columns **from the original matrix**. Reduction tells you *which* columns to keep, not *what they are*.

### Free checks

Before touching any arithmetic:

| | Verdict |
|---|---|
| Set contains $\mathbf 0$ | dependent |
| One vector is a scalar multiple of another | dependent |
| **More than $n$ vectors in an $n$-dimensional space** | **dependent, guaranteed** |

### The engineering translation

**Linear dependence *is* multicollinearity.** A dependent column is one your other columns can already reconstruct — `total = subtotal + tax`. It carries no new information, makes $X^\top X$ singular, and leaves your regression coefficients unidentifiable.

---

## 5. Span, Basis, Dimension

### Span

$$\text{span}\{x_1,\dots,x_k\}=\left\{\sum_i\lambda_ix_i : \lambda_i\in\mathbb{R}\right\}$$

Everything reachable by scaling and adding. Always a subspace.

If every $v\in V$ is such a combination, the set is a **generating set** of $V$.

### Basis

A **basis** is a generating set that is also linearly independent — equivalently, a **minimal** generating set.

Two one-directional effects explain why this is the right notion. When you add a vector to a set:

- **Span** can only grow or stay the same. It never shrinks.
- **Independence** can only be lost or stay. It's never gained.

So more vectors make spanning **easier** and independence **harder**. A basis is exactly the balance point where you have enough to span and few enough to stay independent.

### Why independence matters: uniqueness

If $B$ is a basis, every vector has **exactly one** representation.

Take $S=\{(1,0),(0,1),(1,1)\}$ in $\mathbb{R}^2$ — this spans, but isn't independent. Then

$$(2,1)=2(1,0)+1(0,1)+0(1,1) \qquad\text{and}\qquad (2,1)=1(1,0)+0(0,1)+1(1,1)$$

Two different coordinate triples for the same vector. It's a table with no primary key — everything downstream that relies on coordinates being well-defined breaks.

### Dimension — the single most common confusion

$$\dim(V)=\text{the number of vectors in \textbf{any} basis of } V$$

All bases of the same space have the same size. That's a theorem, and it's what makes "dimension" well-defined.

Read $\dim V$ as **"the required headcount for a basis"**.

**Worked example from your notes.** $U=\text{span}\{x_1,x_2,x_3\}\subseteq\mathbb{R}^3$ with

$$x_1=\begin{bmatrix}1\\2\\-1\end{bmatrix},\quad x_2=\begin{bmatrix}2\\-1\\1\end{bmatrix},\quad x_3=\begin{bmatrix}3\\-4\\3\end{bmatrix}$$

$$\begin{bmatrix}1&2&3\\2&-1&-4\\-1&1&3\end{bmatrix}\to\begin{bmatrix}\mathbf 1&2&3\\0&\mathbf 1&2\\0&0&0\end{bmatrix}$$

Two pivots. Basis $\{x_1,x_2\}$, and $\dim(U)=2$.

Now the confusion. There are **two different dimensions** in play:

| Question | Answer |
|---|---|
| How many **components** does each vector have? | **3** — they live in $\mathbb{R}^3$ |
| What is $\dim(\mathbb{R}^3)$? | **3** — the **ambient** space |
| How many **pivots**? | **2** |
| What is $\dim(U)$? | **2** — $U$ is a **plane** inside $\mathbb{R}^3$ |

$$\boxed{\dim=\text{number of basis vectors}=\text{number of independent directions}}$$

**Not** the number of components.

```
        z
        │      ╱───────────────╱
        │     ╱   U, a plane  ╱      A point on the paper needs
        │    ╱   dim(U) = 2  ╱       3 numbers to locate it in the
        │   ╱                ╱       ROOM, but only 2 to locate it
        O──╱────────────────╱─── y   ON THE PAPER. Those 2 are its
       ╱      R³, dim = 3            coordinates in the basis {x₁,x₂}.
      x
```

Your version: a table with 3 columns where `col3 = 2·col2 − col1`. Three columns, but only **two independent** ones. The data genuinely lives in a 2D subspace even though every row has three entries.

Always: $U\subseteq\mathbb{R}^n \Rightarrow \dim(U)\le n$, with equality only when $U$ is all of $\mathbb{R}^n$.

### The counting rule

For $k$ vectors in an $n$-dimensional space:

| | Verdict |
|---|---|
| $k<n$ | too few to span |
| $k>n$ | must be dependent |
| $k=n$ | possible — now check rank |

This is free. Do it before any elimination. It's also the trap in "if $S$ spans $V$ and each $s_i\in\mathbb{R}^n$ with $n=\dim V$, then $S$ is a basis" — that hypothesis constrains the **width** of each vector, and says nothing at all about **how many** there are.

### Canonical basis and coordinates

$$\mathcal B_1=\{e_1,e_2\}=\left\{\begin{bmatrix}1\\0\end{bmatrix},\begin{bmatrix}0\\1\end{bmatrix}\right\}$$

"Canonical" means the standard choice requiring no arbitrary decisions. It's special because **coordinates in the canonical basis are just the components**:

$$\begin{bmatrix}4\\-1\\2\end{bmatrix}=4e_1+(-1)e_2+2e_3$$

No work required. That's why you normally never think about bases at all — you're silently in the canonical one.

Other bases are equally valid, just less convenient. For an ordered basis $B=(b_1,\dots,b_n)$, writing $x=\alpha_1b_1+\cdots+\alpha_nb_n$ gives the **coordinate vector** $\alpha=(\alpha_1,\dots,\alpha_n)^\top$.

**Worked example from your notes.** $a=(2,1)^\top$ with $B_A=\left\{\begin{bmatrix}1\\-1\end{bmatrix},\begin{bmatrix}1\\1\end{bmatrix}\right\}$:

$$\begin{bmatrix}1&1\\-1&1\end{bmatrix}\begin{bmatrix}\alpha_1\\\alpha_2\end{bmatrix}=\begin{bmatrix}2\\1\end{bmatrix} \Rightarrow \begin{cases}\alpha_1+\alpha_2=2\\-\alpha_1+\alpha_2=1\end{cases} \Rightarrow \alpha=\begin{bmatrix}1/2\\3/2\end{bmatrix}$$

Check: $\tfrac12(1,-1)^\top+\tfrac32(1,1)^\top=(2,1)^\top$ ✓

> A useful realisation: $(2,1)$ was *already* a coordinate vector — with respect to the canonical basis. Coordinates are always relative to **some** basis. The canonical one is just so default nobody mentions it.

---

## 6. Inner Products, Norms, Distances, Angles

### The dependency chain

This is the order your lecturer uses, and it matters — each object is **built from** the previous one:

$$\text{inner product } \Omega \ \longrightarrow\ \text{norm } \|x\|=\sqrt{\langle x,x\rangle} \ \longrightarrow\ \text{distance } d(x,y)=\|x-y\| \ \longrightarrow\ \text{Cauchy–Schwarz} \ \longrightarrow\ \text{angle } \omega$$

Present them the other way round and $\|x\|=\sqrt{\langle x,x\rangle}$ looks like a coincidence instead of a definition.

### Inner product

$\Omega:V\times V\to\mathbb{R}$ is an inner product if it is **symmetric**, **bilinear**, and **positive definite**:

$$\Omega(x,y)=\Omega(y,x)$$
$$\Omega(x,x)>0 \ \ \forall x\neq\mathbf 0, \qquad \Omega(\mathbf 0,\mathbf 0)=0$$
$$\Omega(\lambda x+\psi y,\,z)=\lambda\Omega(x,z)+\psi\Omega(y,z) \quad\text{(and likewise in the second argument)}$$

The **dot product** is the standard inner product on $\mathbb{R}^n$:

$$\langle x,y\rangle=x^\top y=\sum_{i=1}^N x_iy_i$$

Shapes: $(1\times n)(n\times1)=(1\times1)$, a scalar. Two vectors in, one number out.

**What it measures:** how much the two vectors **agree in direction**. This is a property of a *relationship between two* vectors — unlike the norm, which is a property of *one*. Keep that distinction; the whole of §6 turns on it.

### Norm

$$\|x\|=\sqrt{\langle x,x\rangle} \qquad\text{— every inner product \textbf{induces} a norm}$$

A norm is a function taking one vector to a single non-negative number: its **length**. The axioms:

1. **Absolutely homogeneous:** $\|\lambda x\|=\lvert\lambda\rvert\cdot\|x\|$ — double the vector, double the length
2. **Triangle inequality:** $\|x+y\|\le\|x\|+\|y\|$ — a detour is never shorter
3. **Positive definite:** $\|x\|\ge0$, and $\|x\|=0$ only when $x=\mathbf 0$

The family:

| Norm | Formula | For $(3,4)$ | Meaning |
|---|---|---|---|
| $\|x\|_1$ | $\sum_i\lvert x_i\rvert$ | $7$ | Manhattan — walking the city grid |
| $\|x\|_2$ | $\sqrt{\sum_i x_i^2}$ | $5$ | Euclidean — as the crow flies |
| $\|x\|_\infty$ | $\max_i\lvert x_i\rvert$ | $4$ | largest single component |

$\|x\|$ with no subscript means $\|x\|_2$.

### Unit balls

The set $\{x:\|x\|=1\}$ — all points at distance exactly 1 from the origin. Note it's the **boundary**, not a filled region.

By symmetry (every norm uses $\lvert x_i\rvert$), solve in the first quadrant and reflect. All three cross the axes at the same four points; they differ **on the diagonal**:

| Norm | On the diagonal $(t,t)$ | $t=$ |
|---|---|---|
| $L_1$ | $2t=1$ | $0.5$ |
| $L_2$ | $\sqrt{2t^2}=1$ | $1/\sqrt2\approx0.707$ |
| $L_\infty$ | $\max(t,t)=1$ | $1$ |

```
  ┌───────────────┐   p = ∞   square, corners at (±1,±1)
  │   ╭───────╮   │   p = 2   circle, radius 1
  │  ╱  ╱───╲  ╲  │   p = 1   diamond, |x|+|y| = 1
  │ │  │  ·  │  │ │   p = ½   concave — violates the triangle
  │  ╲  ╲───╱  ╱  │           inequality, so NOT a norm
  │   ╰───────╯   │
  └───────────────┘   ‖x‖∞ ≤ ‖x‖₂ ≤ ‖x‖₁  ⟹  B₁ ⊆ B₂ ⊆ B∞
```

Larger norm value ⟹ smaller vector needed to reach 1 ⟹ tighter ball. The three sets are **nested**, touching only at the four axis points. If yours cross anywhere else, you've made an error.

> **Why ML cares.** Least squares and RMSE minimise the $L_2$ norm of residuals. Ridge penalises $\|\beta\|_2$; Lasso penalises $\|\beta\|_1$. Lasso produces **sparse** coefficients precisely because the $L_1$ ball has **corners on the axes** — a constrained optimum tends to land at a corner, where some coordinates are exactly zero. The picture above is the entire explanation.

### Distance

$$d(x,y)=\|x-y\|$$

Properties, all inherited from the norm axioms:

1. $d(x,y)\ge0$, and $d(x,y)=0\iff x=y$
2. $d(x,y)=d(y,x)$ — symmetric
3. $d(x,z)\le d(x,y)+d(y,z)$ — triangle inequality

From your notes: $a=(2,1)^\top$, $b=(-0.5,1)^\top$ gives $a-b=(2.5,0)^\top$, so $d(a,b)=2.5$.

### Cauchy–Schwarz — what it's actually for

$$\lvert\langle x,y\rangle\rvert\le\|x\|\,\|y\|$$

**What it says:** the inner product can never exceed the product of the two lengths. A ceiling.

**Why anyone cares.** You want to define the angle between two vectors by rearranging $\langle x,y\rangle=\|x\|\|y\|\cos\omega$ into

$$\cos\omega=\frac{\langle x,y\rangle}{\|x\|\,\|y\|}$$

But $\cos$ only takes values in $[-1,1]$. If that fraction could ever be $1.4$, no angle $\omega$ would produce it and the definition would collapse.

Cauchy–Schwarz guarantees $-1\le\frac{\langle x,y\rangle}{\|x\|\|y\|}\le1$, so a **unique** $\omega\in[0,\pi]$ always exists.

> **In one sentence: Cauchy–Schwarz is what makes "angle" well-defined.** That's its job in this course. It works in any inner product space, including ones with no geometry you can picture.

Three consequences:

- Cosine similarity is bounded in $[-1,1]$ — that's why the metric is interpretable
- The triangle inequality for the induced norm is proved *using* it
- **Equality holds iff $x,y$ are linearly dependent** — the exam-relevant one

For the equality case: if $y=\lambda x$ then

$$\lvert\langle x,y\rangle\rvert=\lvert\langle x,\lambda x\rangle\rvert=\lvert\lambda\rvert\langle x,x\rangle=\lvert\lambda\rvert\,\|x\|_2^2=\|x\|_2\,\|\lambda x\|_2=\|x\|_2\|y\|_2$$

Hitting the ceiling means the vectors are parallel.

### Angles and orthogonality

$$\boxed{\cos(\omega)=\frac{\langle x,y\rangle}{\|x\|\,\|y\|}}$$

| $\cos\omega$ | $1$ | $0$ | $-1$ |
|---|---|---|---|
| $\omega$ | $0°$ | $90°$ | $180°$ |

**Law of cosines** — worth deriving once rather than memorising:

$$\|x-y\|^2=(x-y)^\top(x-y)=x^\top x-x^\top y-y^\top x+y^\top y=\langle x,x\rangle-2\langle x,y\rangle+\langle y,y\rangle$$
$$=\|x\|^2+\|y\|^2-2\langle x,y\rangle$$

Comparing with the geometric form $\|x\|^2+\|y\|^2-2\|x\|\|y\|\cos\omega$ gives the cosine formula directly.

**Orthogonality:** $x\perp y \iff \langle x,y\rangle=0$. If additionally $\|x\|=\|y\|=1$, they're **orthonormal**.

From your notes: $a=(2,1)^\top$, $b=(-0.5,1)^\top$ gives $\langle a,b\rangle=-1+1=0$, so $\omega=90°$.

**Orthonormal basis:** $\langle b_i,b_j\rangle=0$ for $i\neq j$, and $\langle b_i,b_i\rangle=1$. These are worth constructing because coordinates become free:

$$v=\sum_i\langle v,e_i\rangle e_i$$

Each coordinate is just a dot product — no linear system to solve. Compare that with row-reducing $[A\mid v]$ for a general basis.

Two more consequences worth holding:

- **Orthogonal (non-zero) vectors are automatically independent.** No vector can be built from the others because none has any component in their directions. Independence for free, no elimination needed.
- **Pythagoras:** $x\perp y \Rightarrow \|x+y\|^2=\|x\|^2+\|y\|^2$. This is what makes $\text{Total SS}=\text{Explained SS}+\text{Residual SS}$ true in regression. $R^2$ exists because of orthogonality.

### The trap worth internalising

> $\|x\|_2=\|y\|_2$ does **not** imply $\langle x,y\rangle=\|x\|_2\|y\|_2$.

The hypothesis constrains **length**. The conclusion requires the same **direction** ($\cos\omega=1$). Those are different things.

Counterexample: $(1,0)$ and $(0,1)$ both have norm 1, inner product 0.

The decisive version: in any embedding index you L2-normalise everything, so **every** pair satisfies $\|x\|=\|y\|=1$. If the claim were true, every pair of documents would have cosine similarity 1. Observed similarities span $[-1,1]$.

---

## 7. Projections

### Definition

Let $U\subseteq V$ be a subspace. A linear mapping $\pi:V\to U$ is a **projection** if

$$\pi^2=\pi\circ\pi=\pi$$

*Applying it twice equals applying it **once***. Once you're already in $U$, projecting again changes nothing.

### Projecting onto a line

Given $U=\text{span}\{b\}$ in $\mathbb{R}^2$, we want, for each $x$, the point $\pi_U(x)\in U$ minimising $\|x-\pi_U(x)\|$.

Since $\pi_U(x)\in U$, it must be $\lambda b$ for some $\lambda\in\mathbb{R}$. We call $\lambda$ the **coordinate** of $\pi_U(x)$ in $U$. So the whole problem is finding one number.

**The key move: the minimiser is the one whose residual is orthogonal to $b$.**

$$\langle x-\lambda b,\ b\rangle=0$$
$$\langle x,b\rangle-\lambda\langle b,b\rangle=0$$
$$\boxed{\lambda=\frac{\langle x,b\rangle}{\langle b,b\rangle}=\frac{b^\top x}{b^\top b}}$$

(The denominator is safe: $\langle b,b\rangle=\sum b_i^2>0$ for $b\neq\mathbf 0$.)

Then the projection itself:

$$\pi_U(x)=\lambda b=b\lambda=b\,\frac{b^\top x}{\|b\|_2^2}=\frac{bb^\top}{\|b\|_2^2}\,x=P_\pi x, \qquad \boxed{P_\pi=\frac{bb^\top}{b^\top b}}$$

> ⚠️ **$b^\top b$ is a scalar** — an inner product, $(1\times n)(n\times1)$. **$bb^\top$ is an $n\times n$ matrix** — an outer product, $(n\times1)(1\times n)$. Same two symbols, opposite order, completely different objects. Check the shapes before writing anything down.

### Worked example from your notes

$U=\text{span}\{(1,2,3)^\top\}$ in $\mathbb{R}^3$, projecting $x=(1,4,2)^\top$.

**1. Build the projection matrix.**
$$bb^\top=\begin{bmatrix}1\\2\\3\end{bmatrix}\begin{bmatrix}1&2&3\end{bmatrix}=\begin{bmatrix}1&2&3\\2&4&6\\3&6&9\end{bmatrix}, \qquad \|b\|_2^2=b^\top b=1+4+9=14$$
$$P_\pi=\tfrac1{14}\begin{bmatrix}1&2&3\\2&4&6\\3&6&9\end{bmatrix}$$

**2. Project.**
$$P_\pi x=\tfrac1{14}\begin{bmatrix}15\\30\\45\end{bmatrix}=\tfrac{15}{14}\begin{bmatrix}1\\2\\3\end{bmatrix}$$

**3. Confirm via $\lambda$.**
$$b^\top x=1\cdot1+2\cdot4+3\cdot2=15 \Rightarrow \lambda=\tfrac{15}{14} \ \checkmark$$

Both routes agree, as they must.

The **distance from $x$ to $U$** is $\|r\|$ where $r=x-\pi_U(x)$.

### Projecting onto a subspace

With basis vectors as columns of $A$:

$$P=A(A^\top A)^{-1}A^\top, \qquad \beta=(A^\top A)^{-1}A^\top x$$

The condition is the same — residual orthogonal to $U$ — but checking orthogonality against **every** $u\in U$ is impossible. It's enough to check the **spanning vectors**, because any $u=\sum_jc_jx_j$ gives

$$\langle u, r\rangle=\sum_j c_j\underbrace{\langle x_j,r\rangle}_{=0}=0$$

Orthogonal to each basis vector ⟹ orthogonal to every combination.

### Properties of projection matrices

| | Why |
|---|---|
| $P^\top=P$ | symmetric — read off the formula |
| $P^2=P$ | idempotent — projecting twice changes nothing |
| Eigenvalues are only $1$ and $0$ | $1$ on $U$ (unchanged), $0$ on $U^\perp$ (annihilated) |
| $\text{rk}(P)=\text{tr}(P)=\dim U$ | |

**Worked (from the problem set).** $A=\begin{bmatrix}1&0\\1&1\\0&1\end{bmatrix}$:

$$A^\top A=\begin{bmatrix}2&1\\1&2\end{bmatrix}, \qquad (A^\top A)^{-1}=\tfrac13\begin{bmatrix}2&-1\\-1&2\end{bmatrix}, \qquad P=\tfrac13\begin{bmatrix}2&1&-1\\1&2&1\\-1&1&2\end{bmatrix}$$

Eigenvalues $1$ (multiplicity 2) and $0$ (multiplicity 1); $\text{rk}(P)=2=\text{rk}(A)$.

### Why this is the whole of least squares

```
        y
        ↑╲                 y = ŷ + r,   ŷ ∈ U,   r ∈ U⊥
        │ ╲  r = y - ŷ
        │  ╲               "closest point in U" and "residual
   ─────┴───●──────── U     perpendicular to U" are the SAME
            ŷ               condition. That equivalence is the
                            entire content of least squares.
```

In regression, $U=\text{im}(X)$ is the set of every prediction your model can make. Your $y$ almost certainly isn't in it, so $X\beta=y$ has no exact solution — you project onto the nearest reachable point instead.

Imposing $X^\top(y-X\beta)=\mathbf 0$ gives the **normal equations** $X^\top X\beta=X^\top y$, and hence $\beta=(X^\top X)^{-1}X^\top y$ with hat matrix $P=X(X^\top X)^{-1}X^\top$.

**Why $X^\top X$ is invertible** (when the columns of $X$ are independent) — and this trick is worth learning as a reflex:

$$X^\top Xv=\mathbf 0 \ \Rightarrow\ v^\top X^\top Xv=0 \ \Rightarrow\ (Xv)^\top(Xv)=\|Xv\|_2^2=0 \ \Rightarrow\ Xv=\mathbf 0 \ \Rightarrow\ v=\mathbf 0$$

You can't "cancel" a matrix, but left-multiplying by $v^\top$ converts the equation into a **squared norm**, where zero forces the vector itself to be zero. The same move appears in at least four problems across your sets.

---

## 8. Linear Mappings, Kernel and Image

### Definition

$$\Phi:V\to W \text{ is \textbf{linear}} \iff \Phi(\lambda x+\psi y)=\lambda\Phi(x)+\psi\Phi(y) \quad\forall x,y\in V,\ \lambda,\psi\in\mathbb{R}$$

"Structure-preserving": it doesn't matter whether you combine first and map, or map first and combine.

### The two subspaces

| | $\ker\Phi$ | $\text{im}\,\Phi$ |
|---|---|---|
| **Definition** | $\{x\in V:\Phi(x)=\mathbf 0\}$ | $\{\Phi(x)\}=\text{span}\{\text{columns}\}$ |
| **Lives in** | $V$ — the **input** space | $W$ — the **output** space |
| **Plain English** | everything crushed to zero | everything reachable |
| **From a REF** | **free** columns, parametrised | **pivot** columns of the **original** |
| **Dimension** | nullity | rank |

> They live in **different spaces**. For $\Phi:\mathbb{R}^3\to\mathbb{R}^2$, kernel vectors have three entries and image vectors have two. If yours don't, something has gone wrong. This is the single most common error here.

### Computing them

One row reduction answers both. Reduce, then read in two directions:

1. Reduce to REF
2. Count pivots → rank → $\dim\text{im}$
3. $\dim\ker=\#\text{columns}-\text{rank}$ — **do this before computing the basis**, so you know how many vectors to expect
4. **Image basis** = pivot columns, from the **original** matrix
5. **Kernel basis** — continue to RREF, then for each free variable set it to $1$ and the others to $0$, and fill in the basic variables

### Why set the free variable to 1?

Because it's a **parametrisation**, and the 1 is just a tidy choice.

Take the RREF $\begin{bmatrix}1&0&1\\0&1&1\\0&0&0\end{bmatrix}$. As equations: $x_1+x_3=0$, $x_2+x_3=0$, and $0=0$.

Three unknowns, two real constraints. Nothing pins down $x_3$ — so set $x_3=t$, any real number:

$$x=\begin{bmatrix}-t\\-t\\t\end{bmatrix}=t\begin{bmatrix}-1\\-1\\1\end{bmatrix}$$

Every kernel vector is a multiple of $(-1,-1,1)^\top$. The kernel is a **line through the origin**; $t=1$ just names it without fractions. $t=2$ would give $(-2,-2,2)^\top$, spanning the identical line.

With two free variables you set one to 1 and the rest to 0 in turn — that isolates each independent direction, and the resulting $1/0$ pattern in the free slots guarantees the basis vectors are independent, so you never need to check.

**One free variable = one dimension of freedom = one basis vector.**

### Rank–nullity

$$\dim V=\dim(\text{im}\,\Phi)+\dim(\ker\Phi)$$

Every input dimension is either **preserved** (into the image) or **crushed** (into the kernel). The pivot/free split of the columns *is* this theorem. Use it as a consistency check on every question.

### Injective, surjective, bijective — with a cheap test

For general functions, checking injectivity means checking every pair of inputs. For **linear** maps there's a shortcut.

**Injective $\iff\ker\Phi=\{\mathbf 0\}$.**

Suppose two inputs collide. Then by linearity:

$$\Phi(x_1)=\Phi(x_2) \Rightarrow \Phi(x_1)-\Phi(x_2)=\mathbf 0 \Rightarrow \Phi(x_1-x_2)=\mathbf 0 \Rightarrow x_1-x_2\in\ker\Phi$$

So **the difference of any two colliding inputs lies in the kernel**. If the kernel is trivial, $x_1=x_2$ — they weren't distinct after all.

Conversely, if some $v\neq\mathbf 0$ is in the kernel, then for **any** $x$:

$$\Phi(x+v)=\Phi(x)+\underbrace{\Phi(v)}_{=\mathbf 0}=\Phi(x)$$

$x$ and $x+v$ collide — and you get one such pair for every $x$ in the domain.

> **The insight: because the map is linear, one collision implies collisions everywhere.** A single kernel vector can be added to any input to manufacture a duplicate. That's why inspecting **one point** — the origin — settles injectivity globally.

Hash-function version: if any non-zero $v$ hashes to zero, then `hash(x + v) == hash(x)` for every key. Trivial kernel means no such collision generator exists.

```
  ker = {0}                    ker = span{v}

   x₁ ──→ ●                     x  ──╲
   x₂ ──→ ●                          ●  ← both land here
   x₃ ──→ ●                   x + v ──╱
   all distinct                every input has a twin
```

**The full picture:**

| | Condition | In REF | Shape needed |
|---|---|---|---|
| **Injective** | $\ker=\{\mathbf 0\}$, rank $=\dim V$ | pivot in every **column** | $\dim W\ge\dim V$ |
| **Surjective** | $\text{im}=W$, rank $=\dim W$ | pivot in every **row** | $\dim V\ge\dim W$ |
| **Bijective** | both | square, $\det\neq0$ | $\dim V=\dim W$ |

**Columns for injective, rows for surjective.** Same reduction, read two ways.

Shape alone gives free answers: a **tall** map ($\dim W>\dim V$) can never be surjective — not enough columns to fill the bigger space. A **wide** map can never be injective — it must crush a dimension. State this before computing.

### Worked — the two 3×3 maps

$$A_\Phi=\begin{bmatrix}1&2&0\\0&1&0\\1&0&1\end{bmatrix}: \quad \det=1\neq0 \Rightarrow \ker\Phi=\{\mathbf 0\},\ \text{im}\,\Phi=\mathbb{R}^3 \Rightarrow \textbf{bijective}$$

$$B_{\Phi'}=\begin{bmatrix}1&2&3\\0&1&1\\1&3&4\end{bmatrix}: \quad \det=0 \Rightarrow \text{non-trivial kernel}$$

$$\xrightarrow{R_3-R_1}\begin{bmatrix}1&2&3\\0&1&1\\0&1&1\end{bmatrix} \xrightarrow{R_3-R_2}\begin{bmatrix}1&2&3\\0&1&1\\0&0&0\end{bmatrix} \xrightarrow{R_1-2R_2}\begin{bmatrix}\mathbf 1&0&1\\0&\mathbf 1&1\\0&0&0\end{bmatrix}$$

$x_1+x_3=0$, $x_2+x_3=0$, $x_3=t$ free:

$$\ker\Phi'=\text{span}\left\{\begin{bmatrix}-1\\-1\\1\end{bmatrix}\right\}, \qquad \text{im}\,\Phi'=\text{span}\left\{\begin{bmatrix}1\\0\\1\end{bmatrix},\begin{bmatrix}2\\1\\3\end{bmatrix}\right\}$$

> **The kernel vector is a recipe for the redundant column.** $-c_1-c_2+c_3=\mathbf 0$ means $c_3=c_1+c_2$, and indeed $(3,1,4)=(1,0,1)+(2,1,3)$. Column 3 was redundant all along — which is why it has no pivot and is excluded from the image basis.
>
> **Trivial kernel ⟺ no redundancy ⟺ independent columns ⟺ injective.** One chain, four vocabularies.

### Worked — a map between different dimensions

$$B=\begin{bmatrix}1&1&1\\0&1&1\end{bmatrix}, \qquad S:\mathbb{R}^3\to\mathbb{R}^2$$

Already in REF, pivots in columns 1 and 2, so $\text{rk}(B)=2$ and column 3 is free.

$$x_1=0,\ x_2+x_3=0 \Rightarrow \ker S=\text{span}\left\{\begin{bmatrix}0\\-1\\1\end{bmatrix}\right\} \subseteq\mathbb{R}^3$$

$$c_3=c_2, \text{ so } \ \text{im}\,S=\text{span}\left\{\begin{bmatrix}1\\0\end{bmatrix},\begin{bmatrix}1\\1\end{bmatrix}\right\}=\mathbb{R}^2$$

**Not injective** — $\dim\ker S=1$, and concretely $S(0,0,0)^\top=S(0,-1,1)^\top=(0,0)^\top$.
**Surjective** — $\dim(\text{im}\,S)=2=\dim\mathbb{R}^2$.
Consistency: $1+2=3=\dim\mathbb{R}^3$ ✓

This is the counterexample to "surjective ⟹ injective".

### Transformation matrix

Let $V,W$ have **ordered** bases $B=(b_1,\dots,b_n)$ and $C=(c_1,\dots,c_m)$, with $\Phi:V\to W$ linear. For each $j$:

$$\Phi(b_j)=\alpha_{1j}c_1+\cdots+\alpha_{mj}c_m=\sum_{i=1}^m\alpha_{ij}c_i$$

This is the **unique** representation of $\Phi(b_j)$ with respect to $C$ — unique because $C$ is a basis. The $m\times n$ matrix $A_\Phi$ with entries $\alpha_{ij}$ is the **transformation matrix of $\Phi$**.

Its **$j$-th column is the coordinate vector of $\Phi(b_j)$ with respect to $C$**. So: *apply $\Phi$ to each basis vector, write the answer in $C$-coordinates, stack as columns.*

$$\boxed{\hat y=A_\Phi\,\hat x}$$

> ⚠️ **This relates coordinates, not the vectors themselves.** $\hat x$ is $x$'s coordinate vector wrt $B$; $\hat y$ is $y$'s wrt $C$. Your notes underline this, and it's easy to lose marks on.

---

## 9. Matrix Operations

### Addition

Element-wise, and **dimensions must match**:

$$A+B=[a_{ij}+b_{ij}], \qquad A,B\in\mathbb{R}^{m\times n}$$

### Multiplication — two readings

$$A\in\mathbb{R}^{m\times n},\ B\in\mathbb{R}^{n\times k}, \qquad C=AB\in\mathbb{R}^{m\times k}, \qquad c_{ij}=\sum_{l=1}^n a_{il}b_{lj}$$

Inner dimensions must match: $(m\times n)(n\times k)=(m\times k)$.

The row-times-column reading is how you compute. **The column reading is how you understand:**

$$Ab=\begin{bmatrix}A_{\cdot1}&A_{\cdot2}&\cdots&A_{\cdot n}\end{bmatrix}\begin{bmatrix}b_1\\\vdots\\b_n\end{bmatrix}=b_1A_{\cdot1}+b_2A_{\cdot2}+\cdots+b_nA_{\cdot n}$$

**$Ab$ is always a linear combination of $A$'s columns, weighted by $b$.** Matrix–matrix multiplication does this once per column of $B$.

This single fact explains why $\text{im}(A)=\text{span}\{\text{columns of } A\}$, and it's the fact you use whenever a problem says "explain why $\hat y=X\beta$".

### Structural properties

| | |
|---|---|
| **Associative** | $(AB)C=A(BC)$ |
| **Distributive** | $(A+B)C=AC+BC$, $\ A(C+D)=AC+AD$ |
| **NOT commutative** | $AB\neq BA$ in general |
| **Identity** | $I_mA=AI_n=A$ |
| **Scalar** | $\lambda A=K$ with $k_{ij}=\lambda a_{ij}$ |

**Why associativity is not a triviality.** Your notes give the example: $A\in\mathbb{R}^{n\times k}$ with $n=100{,}000$ and $k=5$.

- $(AA^\top)x$ — builds a $100{,}000\times100{,}000$ matrix first. Ten billion entries.
- $A(A^\top x)$ — the inner product is $k\times1$; nothing ever exceeds $k$-sized intermediates.

Identical answer, wildly different cost. Associativity is what licenses the rewrite, and choosing the bracketing *is* the optimisation. This is the same instinct as pushing a filter down before a join.

### Transpose

$$B=A^\top \iff b_{ij}=a_{ji}$$

$$(A^\top)^\top=A \qquad (A+B)^\top=A^\top+B^\top \qquad \boxed{(AB)^\top=B^\top A^\top}$$

**The order reverses.** Same for inverses: $(AB)^{-1}=B^{-1}A^{-1}$. Think of undoing a sequence of operations — you reverse the steps.

### Symmetric matrices

$A=A^\top$ — square only. Example: $\begin{bmatrix}2&1\\1&2\end{bmatrix}$.

**For every $A\in\mathbb{R}^{m\times n}$, both $A^\top A$ and $AA^\top$ are symmetric:**

$$(A^\top A)^\top=A^\top(A^\top)^\top=A^\top A \ \checkmark \qquad (AA^\top)^\top=(A^\top)^\top A^\top=AA^\top \ \checkmark$$

This matters enormously: it means covariance matrices, Gram matrices, and Hessians all inherit the spectral theorem's guarantees (§11).

| | |
|---|---|
| **Sum** of symmetric matrices | always symmetric ✓ |
| **Product** of symmetric matrices | **not** always symmetric ✗ |

---

## 10. Inverse, Trace, Determinant, Rank, Orthogonal Matrices

### Inverse

$AA^{-1}=A^{-1}A=I$, square matrices only.

$$A=\begin{bmatrix}a&b\\c&d\end{bmatrix} \Rightarrow A^{-1}=\frac{1}{\det(A)}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$$

Swap the diagonal, negate the off-diagonal, divide by the determinant. It exists **iff $\det A\neq0$** — which is exactly when that division is legal.

> ⚠️ $(X^\top X)^{-1}\neq X^{-1}(X^\top)^{-1}$ when $X$ isn't square. $X$ has no inverse at all; $(X^\top X)^{-1}$ is a single indivisible object.

### Trace

$$\text{tr}(A)=\sum_{i=1}^n a_{ii}$$

The sum of the diagonal. Off-diagonal entries are ignored entirely.

| Property | |
|---|---|
| $\text{tr}(A+B)=\text{tr}(A)+\text{tr}(B)$, $\ \text{tr}(\lambda A)=\lambda\,\text{tr}(A)$ | **linear operator** |
| $\text{tr}(I_n)=n$ | |
| $\text{tr}(AB)=\text{tr}(BA)$ | for $A\in\mathbb{R}^{n\times k}$, $B\in\mathbb{R}^{k\times n}$ |
| $\text{tr}(B^{-1}AB)=\text{tr}(A)$ | **invariant under basis change** |
| $\text{tr}(xy^\top)=y^\top x$ | outer product → inner product |

**Why $\text{tr}(AB)=\text{tr}(BA)$ holds even when the products are different sizes.** With $A$ being $m\times n$ and $B$ being $n\times m$, $AB$ is $m\times m$ and $BA$ is $n\times n$ — yet:

$$\text{tr}(AB)=\sum_i\sum_j a_{ij}b_{ji} \qquad \text{tr}(BA)=\sum_j\sum_i b_{ji}a_{ij}$$

The same double sum, summed in the other order. The entries are scalars, so they commute — which is why this works even though $AB\neq BA$ as matrices.

**Cyclic, not arbitrary.** $\text{tr}(ABC)=\text{tr}(BCA)=\text{tr}(CAB)$ ✓, but $\text{tr}(ABC)\neq\text{tr}(ACB)$ in general. Rotate the order; never reshuffle it.

The basis-invariance $\text{tr}(B^{-1}AB)=\text{tr}(A)$ follows immediately from cyclicity, and it's conceptually important: **trace is a property of the linear map, not of the basis you chose to write it in.** That's why it turns out to equal $\sum\lambda_i$.

### Determinant

The determinant of a square $A\in\mathbb{R}^{n\times n}$ is:

- a function mapping $A$ onto the real line
- the **volume-scaling factor** of the transformation $x\mapsto Ax$, with the **sign** indicating whether orientation is preserved or reversed

$$\lvert A\rvert=\det(A)=a_{11}a_{22}-a_{12}a_{21} \qquad \det\begin{bmatrix}1&2\\3&4\end{bmatrix}=(1\cdot4)-(2\cdot3)=-2$$

**Why "volume".** Take the unit square and a diagonal $A=\begin{bmatrix}a_{11}&0\\0&a_{22}\end{bmatrix}$:

$$Ae_1=1\cdot a_1+0\cdot a_2=\begin{bmatrix}a_{11}\\0\end{bmatrix}, \qquad Ae_2=\begin{bmatrix}0\\a_{22}\end{bmatrix}$$

The image is a rectangle of area $a_{11}a_{22}=\lvert A\rvert$.

**What if the columns are dependent?** With $\tilde A=[\tilde a_1\ \ \lambda\tilde a_1]$:

$$\det(\tilde A)=\tilde a_{11}\cdot\lambda\tilde a_{21}-\tilde a_{21}\cdot\lambda\tilde a_{11}=0$$

The $n$-dimensional volume **collapses to zero** — the square is squashed onto a line. Information is destroyed, and the map isn't invertible.

$$\boxed{\det(A)\neq0 \iff A^{-1} \text{ exists}}$$

```
  det ≠ 0                 det = 0
    ╱─────╱                   ↗
   ╱     ╱                  ↗        both columns lie
  ●─────→                 ●───→      on the same line
  real area               zero area
```

**Computing it.**

*3×3 — Sarrus' rule* (three "down-right" diagonals positive, three "up-right" negative):

$$\det(A)=a_{11}a_{22}a_{33}+a_{12}a_{23}a_{31}+a_{13}a_{21}a_{32}-a_{31}a_{22}a_{13}-a_{32}a_{23}a_{11}-a_{33}a_{21}a_{12}$$

⚠️ **3×3 only.** There is no Sarrus rule for 4×4.

*$n\times n$ — Laplace expansion:*

$$\text{along column } j:\quad \det(A)=\sum_{k=1}^n(-1)^{k+j}a_{kj}\det(A_{kj})$$
$$\text{along row } j:\quad \det(A)=\sum_{k=1}^n(-1)^{k+j}a_{jk}\det(A_{jk})$$

where $A_{kj}$ is the submatrix left after deleting row $k$ and column $j$. **Pick the row or column with the most zeros** — each zero kills a whole sub-determinant.

For anything 4×4 or larger, reducing to triangular form and multiplying the diagonal is usually faster than expansion.

**Properties:**

$$\det(AB)=\det A\det B \qquad \det(A)=\det(A^\top) \qquad \det(A^{-1})=\tfrac1{\det A} \qquad \det(\lambda A)=\lambda^n\det A$$

| Operation | Effect |
|---|---|
| Adding multiples of rows/columns to another | **no change** |
| Swapping two rows/columns | **sign flips** |
| Triangular or diagonal | $\det=\prod$ diagonal |

> Note that **column** operations are allowed here, unlike when solving systems. That's because $\det(A)=\det(A^\top)$, so rows and columns play symmetric roles for the determinant specifically.

**Worked.** $M(t)=\begin{bmatrix}1&t&0\\0&1&t\\t&0&1\end{bmatrix}$, expanding along the first row (the zero saves a term):

$$\det M=1\cdot\begin{vmatrix}1&t\\0&1\end{vmatrix}-t\cdot\begin{vmatrix}0&t\\t&1\end{vmatrix}=1-t(0-t^2)=1+t^3$$

Invertible iff $1+t^3\neq0$, which over $\mathbb{R}$ fails only at $t=-1$.

### Rank

> The rank of $A\in\mathbb{R}^{n\times m}$ is the number of **linearly independent columns**, which is equivalent to the number of **linearly independent rows**.

That equivalence — row rank equals column rank — is a genuine theorem and not at all obvious. It's why $\text{rk}(A)=\text{rk}(A^\top)$.

$$A \text{ is \textbf{full rank} if } \text{rk}(A)=\min(n,m) \qquad\qquad A\in\mathbb{R}^{n\times n} \text{ invertible} \iff \text{rk}(A)=n$$

Also: $\text{rk}(A)=\#\text{pivots}=\dim\text{im}(A)$, and $\text{rk}(A)\le\min(n,m)$ — you can't have more pivots than rows or columns.

> ⚠️ **Rank is not the number of non-zero eigenvalues.** $\begin{bmatrix}0&1\\0&0\end{bmatrix}$ has rank 1 but both eigenvalues are 0.

**Worked — how rank deficiency creates a kernel.** Let $B=[\,b_1\ \ b_2\ \ \lambda b_2\,]\in\mathbb{R}^{3\times3}$ with $\lambda\neq0$, so $\text{rk}(B)=2$.

Take any $x=(x_1,x_2,x_3)^\top$ and build $y=\left(x_1,\ x_2-\alpha,\ x_3+\tfrac\alpha\lambda\right)^\top$ with $\alpha\neq0$:

$$Bx=x_1b_1+x_2b_2+x_3\lambda b_2=x_1b_1+(x_2+\lambda x_3)b_2$$
$$By=x_1b_1+(x_2-\alpha)b_2+\left(x_3+\tfrac\alpha\lambda\right)\lambda b_2=x_1b_1+(x_2-\alpha+\lambda x_3+\alpha)b_2=x_1b_1+(x_2+\lambda x_3)b_2$$

Identical. So $\Phi(x)=\Phi(y)$, and by linearity $\Phi(x-y)=\mathbf 0$, meaning the kernel contains

$$v=x-y=\left(0,\ \alpha,\ -\tfrac\alpha\lambda\right)^\top, \qquad Bv=0\cdot b_1+\alpha b_2-\tfrac\alpha\lambda\cdot\lambda b_2=\mathbf 0 \ \checkmark$$

> **This one example contains the whole chapter:** a redundant column ⟹ rank drop ⟹ non-trivial kernel ⟹ distinct inputs colliding ⟹ not injective ⟹ not invertible.

### Orthogonal matrices

$$Q\in\mathbb{R}^{n\times n} \text{ is \textbf{orthogonal} if } QQ^\top=Q^\top Q=I \qquad\Longrightarrow\qquad Q^\top=Q^{-1}$$

The columns are orthonormal. The payoff is that **inverting costs nothing** — just transpose.

| Property | |
|---|---|
| **Preserves length** | $\|Qx\|_2=\|x\|_2$ |
| **Preserves inner product** | $\langle Qx,Qy\rangle=\langle x,y\rangle$ |
| ⟹ | preserves **angles and distances** |
| $\det Q=\pm1$ | volume preserved |

Geometrically these are exactly the **rotations and reflections**. Numerically they're prized because they don't amplify error — which is why QR, SVD and eigendecomposition are built from them.

**The rotation matrix.**

$$R(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}, \qquad R(-\theta)=\begin{bmatrix}\cos\theta&\sin\theta\\-\sin\theta&\cos\theta\end{bmatrix}=R(\theta)^\top$$

$$R(\theta)R(\theta)^\top=\begin{bmatrix}\cos^2\theta+\sin^2\theta&\cos\theta\sin\theta-\sin\theta\cos\theta\\\sin\theta\cos\theta-\cos\theta\sin\theta&\cos^2\theta+\sin^2\theta\end{bmatrix}=\begin{bmatrix}1&0\\0&1\end{bmatrix}=I$$

using $\cos^2\theta+\sin^2\theta=1$ and the off-diagonals cancelling.

**Composition.** $R(\theta_1)R(\theta_2)=R(\theta_1+\theta_2)$ — rotating by $\theta_1$ then $\theta_2$ is one rotation of $\theta_1+\theta_2$. Proving it is a direct multiplication plus the angle-addition identities

$$\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta, \qquad \sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta$$

**The efficient route to the inverse:** don't compute one. Set $\theta_2=-\theta_1$ in the composition rule to get $R(\theta)R(-\theta)=R(0)=I$, hence $R(\theta)^{-1}=R(-\theta)=R(\theta)^\top$.

**Cosine similarity between $x$ and $R(\theta)x$.** Since

$$\langle x,R(\theta)x\rangle=\|x\|^2\cos\theta \qquad\text{and}\qquad \|R(\theta)x\|=\|x\|$$

the similarity is $\dfrac{\|x\|^2\cos\theta}{\|x\|\,\|x\|}=\cos\theta$. Exactly the rotation angle — which is what "preserves angles" means, made concrete.

---

## 11. Eigenvalues and Eigenvectors

### The core idea

A matrix is a **transformation**. It takes vectors and moves them. Most get **rotated and stretched**. An **eigenvector** is a special direction that only gets **stretched** — never rotated. The stretch factor $\lambda$ is the **eigenvalue**.

$$Ax=\lambda x, \qquad x\in\mathbb{R}^n\setminus\{\mathbf 0\}$$

```
  generic vector            eigenvector
     ↗ Av                      ↗ Av
    ╱                         ╱
   ╱  ↗ v                    ╱ ↗ v      same line,
  ╱ ╱                       ╱╱          just λ times longer
 O                         O
 direction changed         direction preserved
```

Reading the equation: applying the whole matrix to $x$ does the same thing as multiplying $x$ by a single number. **The matrix collapses to a scalar along that direction.**

> "Eigen" is German for *own* / *characteristic* — the matrix's own directions. Nobody tells you this, so the word carries no meaning until they do.

**Why this is famously hard.** The definition looks trivial, so people assume they're missing something. The real obstacle is that it requires seeing a matrix as a **function**, not as a grid of numbers. Until you make that shift, "special directions" is meaningless. It's also taught computationally first, which buries the idea under arithmetic.

### Finding them

$$Ax=\lambda x \Rightarrow (A-\lambda I_n)x=\mathbf 0$$

($I$ is needed because you can't subtract a scalar from a matrix; $\lambda I$ makes the subtraction legal.)

We need a **non-zero** $x$. But a matrix with a non-trivial kernel is exactly a **singular** one. Hence:

$$\boxed{p_A(\lambda)=\det(A-\lambda I)=0}$$

**That is why determinants appear in eigenvalue problems.** You're hunting for the values of $\lambda$ that make $A-\lambda I$ collapse.

The **characteristic polynomial**:

$$p_A(\lambda)=c_0+c_1\lambda+c_2\lambda^2+\cdots+c_{n-1}\lambda^{n-1}+(-1)^n\lambda^n$$

with two coefficients worth knowing:

$$c_0=\det(A), \qquad c_{n-1}=(-1)^{n-1}\text{tr}(A)$$

**Theorem.** $\lambda\in\mathbb{R}$ is an eigenvalue of $A$ **iff** $\lambda$ is a root of $p_A$.

For 2×2, expanding gives the shortcut:

$$\lambda^2-\text{tr}(A)\,\lambda+\det(A)=0$$

### The two identities

$$\det(A)=\prod_{i=1}^n\lambda_i \qquad\qquad \text{tr}(A)=\sum_{i=1}^n\lambda_i$$

(both with algebraic multiplicities.)

**Why $\det=\prod\lambda_i$:** eigenvalues are the stretch factors along the eigen-directions, and total volume change is the product of the stretches. A zero eigenvalue crushes a direction ⟹ zero volume ⟹ singular.

$$\text{Some } \lambda_i=0 \iff \exists x\neq\mathbf 0 \text{ with } Ax=\mathbf 0 \iff A^{-1} \text{ does not exist}$$

**Use these as an arithmetic check on every eigenvalue computation you do.**

Also: **triangular or diagonal matrices have their eigenvalues on the diagonal**, because $A-\lambda I$ stays triangular and its determinant is the diagonal product $\prod(a_{ii}-\lambda)$.

### The worked example that runs through everything

Your notes use one matrix for the entire topic. Learn it end to end.

$$A=\begin{bmatrix}4&2\\1&3\end{bmatrix}$$

**Step 1 — roots of the characteristic polynomial**

$$\lvert A-\lambda I\rvert=\begin{vmatrix}4-\lambda&2\\1&3-\lambda\end{vmatrix}=(4-\lambda)(3-\lambda)-2=12-7\lambda+\lambda^2-2=\lambda^2-7\lambda+10=(\lambda-2)(\lambda-5)$$

$$\lambda_1=2, \qquad \lambda_2=5$$

Check: $2+5=7=\text{tr}(A)$ ✓ and $2\cdot5=10=\det(A)$ ✓

**Step 2 — eigenvectors, by solving $(A-\lambda I)x=\mathbf 0$**

For $\lambda=2$:
$$\begin{bmatrix}2&2\\1&1\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix} \Rightarrow x_1=-x_2, \quad\text{set } x_2=t: \quad x=t\begin{bmatrix}-1\\1\end{bmatrix}$$
$$E_2=\text{span}\left\{\begin{bmatrix}-1\\1\end{bmatrix}\right\}$$

For $\lambda=5$:
$$\begin{bmatrix}-1&2\\1&-2\end{bmatrix}\begin{bmatrix}x_1\\x_2\end{bmatrix}=\begin{bmatrix}0\\0\end{bmatrix} \Rightarrow x_1=2x_2, \quad\text{set } x_2=t: \quad x=t\begin{bmatrix}2\\1\end{bmatrix}$$
$$E_5=\text{span}\left\{\begin{bmatrix}2\\1\end{bmatrix}\right\}$$

**Step 3 — diagonalize.** Distinct eigenvalues ⟹ the eigenvectors are independent ⟹ they form a basis.

$$P=\begin{bmatrix}1&2\\-1&1\end{bmatrix}, \qquad D=\begin{bmatrix}2&0\\0&5\end{bmatrix}, \qquad \det P=1+2=3, \qquad P^{-1}=\tfrac13\begin{bmatrix}1&-2\\1&1\end{bmatrix}$$

$$PDP^{-1}=\begin{bmatrix}2&10\\-2&5\end{bmatrix}\cdot\tfrac13\begin{bmatrix}1&-2\\1&1\end{bmatrix}=\tfrac13\begin{bmatrix}12&6\\3&9\end{bmatrix}=\begin{bmatrix}4&2\\1&3\end{bmatrix}=A \ \checkmark$$

### Eigenspaces

$$E_\lambda=\ker(A-\lambda I)=\{x: Ax=\lambda x\}$$

**Why the concept exists:** eigenvectors are never unique. If $Ax=\lambda x$ then

$$A(cv)=c\,Av=c\lambda v=\lambda(cv)$$

so every scalar multiple works too. And two eigenvectors for the same $\lambda$ sum to another one. Closed under both operations ⟹ it's a **subspace**. Rather than talk about individual eigenvectors, you talk about the whole space.

> **Not necessarily the span of only one vector** — your notes flag this explicitly, and it's exactly what the multiplicity discussion below is about.

Note $E_\lambda$ contains $\mathbf 0$ (subspaces must), but $\mathbf 0$ is **not** an eigenvector — the definition requires $x\neq\mathbf 0$. Slightly awkward, but standard.

### Multiplicities

| | Meaning |
|---|---|
| **Geometric** $\text{gm}(\lambda_i)$ | number of linearly independent eigenvectors for $\lambda_i$, i.e. $\dim(E_{\lambda_i})$ |
| **Algebraic** $\text{am}(\lambda_i)$ | number of roots of $p_A$ equal to $\lambda_i$ |

$$\boxed{1\le\text{gm}(\lambda_i)\le\text{am}(\lambda_i)}$$

**The contrast pair — same characteristic polynomial, opposite verdicts.**

**Example 1.** $B=\begin{bmatrix}2&0\\0&2\end{bmatrix}$

$$\begin{vmatrix}2-\lambda&0\\0&2-\lambda\end{vmatrix}=(2-\lambda)^2 \Rightarrow \lambda_1=\lambda_2=2, \quad \text{am}(2)=2$$

Finding eigenvectors: $(B-2I)x=\mathbf 0$ becomes $\begin{bmatrix}0&0\\0&0\end{bmatrix}x=\mathbf 0$ — **true for any $v\in\mathbb{R}^2$**.

$$E_2=\mathbb{R}^2=\text{span}\left\{\begin{bmatrix}1\\0\end{bmatrix},\begin{bmatrix}0\\1\end{bmatrix}\right\}, \qquad \text{gm}(2)=\dim(E_2)=2=\text{am}(2)$$

**Example 2.** $C=\begin{bmatrix}2&0\\1&2\end{bmatrix}$

$$\begin{vmatrix}2-\lambda&0\\1&2-\lambda\end{vmatrix}=(2-\lambda)^2-(1)(0)=(2-\lambda)^2 \Rightarrow \lambda_1=\lambda_2=2, \quad \text{am}(2)=2$$

But now $(C-2I)x=\mathbf 0$ becomes $\begin{bmatrix}0&0\\1&0\end{bmatrix}x=\mathbf 0$, forcing $x_1=0$ with $x_2$ free:

$$E_2=\left\{\begin{bmatrix}0\\x_2\end{bmatrix}\right\}=\text{span}\left\{\begin{bmatrix}0\\1\end{bmatrix}\right\}, \qquad \text{gm}(2)=1 < \text{am}(2)=2$$

**$C$ is defective.** Identical polynomial, one extra entry, completely different structure. This is the exam trap.

### Defective and diagonalizable

$A\in\mathbb{R}^{n\times n}$ is **defective** if it possesses fewer than $n$ linearly independent eigenvectors.

Eigenvectors corresponding to **distinct** eigenvalues are linearly independent. So if any $\lambda_i$ has $\text{gm}(\lambda_i)<\text{am}(\lambda_i)$, the matrix is defective.

$$\boxed{\text{defective} \iff \text{no eigenbasis} \iff \text{not diagonalizable}}$$

An **eigenbasis** of $A$ is a basis of $\mathbb{R}^n$ consisting entirely of eigenvectors. To build one: choose a basis for each eigenspace $E_{\lambda_1},\dots,E_{\lambda_k}$; if that yields $n$ independent eigenvectors in total, you have an eigenbasis.

**Diagonalizable** means there's an invertible $P$ with $D=P^{-1}AP$ diagonal. The construction: define $D=\text{diag}(\lambda_1,\dots,\lambda_n)$ and stack the corresponding eigenvectors as columns, $P=[p_1\ p_2\ \cdots\ p_n]$. Then

$$AP=PD \qquad\Longleftrightarrow\qquad A=PDP^{-1}$$

$P$ must be invertible $\iff$ full column rank $\iff$ the eigenvectors form a basis of $\mathbb{R}^n$.

Two facts worth having:

- **$n$ distinct eigenvalues ⟹ diagonalizable.** Sufficient, **not necessary** — $I$ is diagonalizable with all eigenvalues equal.
- **A symmetric matrix can always be diagonalized.** Symmetric matrices are never defective, which is why covariance matrices always decompose cleanly and PCA never hits this problem.

### Properties of the eigendecomposition

Read $A=PDP^{-1}$ right to left as a pipeline: $P^{-1}$ translates into eigen-coordinates, $D$ scales each axis independently, $P$ translates back.

**Powers become trivial:**

$$A^k=(PDP^{-1})^k=PDP^{-1}PDP^{-1}\cdots PDP^{-1}=PD^kP^{-1}=P\,\text{diag}(\lambda_1^k,\dots,\lambda_n^k)\,P^{-1}$$

The inner $P^{-1}P$ pairs collapse to $I$. This is why eigenvalues govern long-run behaviour: $\lvert\lambda\rvert>1$ explodes, $\lvert\lambda\rvert<1$ decays.

**Determinant falls out:**

$$\det(A)=\det(PDP^{-1})=\det(P)\det(D)\det(P^{-1})=\frac{\det(P)\det(D)}{\det(P)}=\det(D)=\prod_{i=1}^n d_{ii}$$

### Eigenvalue identities

All share the same eigenvector:

| If $Ax=\lambda x$ | then | Proof |
|---|---|---|
| | $\lambda^2$ is an eigenvalue of $A^2$ | $A^2x=A(Ax)=\lambda Ax=\lambda^2x$ |
| | $\lambda^{-1}$ is an eigenvalue of $A^{-1}$ | $A^{-1}Ax=\lambda A^{-1}x \Rightarrow A^{-1}x=\tfrac1\lambda x$ |
| | $\lambda+1$ is an eigenvalue of $A+I$ | $Ax+x=\lambda x+x \Rightarrow (A+I)x=(\lambda+1)x$ |
| | $(\lambda-\alpha)^{-1}$ for $(A-\alpha I)^{-1}$ | $(A-\alpha I)x=(\lambda-\alpha)x$, then invert |

**Eigenvalues of $A^\top A$ and $AA^\top$ are non-negative:**

$$A^\top Ax=\lambda x \Rightarrow x^\top A^\top Ax=\lambda x^\top x \Rightarrow \|Ax\|_2^2=\lambda\|x\|_2^2 \Rightarrow \lambda=\frac{\|Ax\|_2^2}{\|x\|_2^2}\ge0$$

> Again the $v^\top A^\top Av=\|Av\|^2$ move. **Learn it as a reflex** — it converts an unmanageable matrix expression into a norm, where you have theorems available. It appears in the $X^\top X$ invertibility proof, the Hessian PSD proof, this one, and the SVD existence argument.

---

## 12. Quadratic Forms and Definiteness

### Quadratic form

$$q_A(x)=x^\top Ax=\sum_{i=1}^n\sum_{j=1}^n a_{ij}x_ix_j, \qquad q_A:\mathbb{R}^n\to\mathbb{R}$$

Vector in, single number out. It's the matrix analogue of $ax^2$ — and like $ax^2$, the interesting question is whether it's always positive, always negative, or neither.

### The four classes

For a **symmetric** $A\in\mathbb{R}^{n\times n}$:

| | Condition | Eigenvalues |
|---|---|---|
| **Positive definite (PD)** | $v^\top Av>0$ for all $v\neq\mathbf 0_n$ | strictly positive |
| **Positive semidefinite (PSD)** | $v^\top Av\ge0$ for all $v\in\mathbb{R}^n$ | non-negative |
| **Negative definite (ND)** | $-A$ is PD | strictly negative |
| **Negative semidefinite (NSD)** | $-A$ is PSD | non-positive |
| **Indefinite** | mixed sign | mixed sign |

> ND and NSD are defined **by negation**. Don't memorise separate criteria — negate the matrix and reuse the PD/PSD test.

The eigenvalue characterisation and the $x^\top Ax$ characterisation are equivalent, and you pick whichever is cheaper. For a 2×2, the trace/determinant signs settle it in seconds.

### Worked examples

$$A=\begin{bmatrix}2&1\\1&3\end{bmatrix}: \quad \text{tr}=5,\ \det=6-1=5 \Rightarrow \lambda_{1,2}=\frac{5\pm\sqrt{25-20}}{2}=\frac{5\pm\sqrt5}{2}>0$$

Both positive ⟹ **PD**.

$$B=\begin{bmatrix}0&0\\0&1\end{bmatrix}: \quad \lambda\in\{1,0\}$$

So $x^\top Bx\ge0$ always, but taking $x=(1,0)^\top$ gives exactly $0$ — not strictly positive. **PSD, not PD.**

$$C=-A: \quad \lambda=-\tfrac{5\pm\sqrt5}{2}<0 \Rightarrow \textbf{ND}$$

$$D=\begin{bmatrix}0&0\\0&-2\end{bmatrix}: \quad \lambda\in\{0,-2\} \Rightarrow \textbf{NSD, not ND} \quad (x=(1,0)^\top \text{ gives } 0)$$

And a diagonal case: $D=\text{diag}(4,1,0)$ has eigenvalues $4,1,0$ read straight off, with

$$E_4=\text{span}\{e_1\}, \qquad E_1=\text{span}\{e_2\}, \qquad E_0=\text{span}\{e_3\}$$

each of dimension 1. Since $\lambda=0$ appears, $D$ is **PSD but not PD** — and correspondingly not invertible.

### The result that matters most

**For any $A\in\mathbb{R}^{n\times m}$, both $A^\top A\in\mathbb{R}^{m\times m}$ and $AA^\top\in\mathbb{R}^{n\times n}$ are symmetric and positive semidefinite — always.**

Symmetric by §9; PSD because $v^\top A^\top Av=\|Av\|_2^2\ge0$.

And the upgrade condition:

$$\text{rk}(A)=m \ \ (\text{full \textbf{column} rank}) \implies A^\top A \text{ is symmetric and \textbf{PD}}$$
$$\text{rk}(A)=n \ \ (\text{full \textbf{row} rank}) \implies AA^\top \text{ is symmetric and \textbf{PD}}$$

The gap between PSD and PD is exactly the gap between "has a kernel" and "doesn't":

$$A^\top A \text{ PD} \iff \|Av\|^2>0 \ \forall v\neq\mathbf 0 \iff Av\neq\mathbf 0 \ \forall v\neq\mathbf 0 \iff \ker(A)=\{\mathbf 0\}$$

> **"$A^\top A$ is positive definite for any $A$" is false** — it's only PSD in general. This is a favourite exam statement, and the fix is one phrase: *needs full column rank*.
>
> In regression terms: full column rank ⟹ $X^\top X$ is PD ⟹ invertible ⟹ unique $\hat\beta$. Rank-deficient ⟹ merely PSD ⟹ singular ⟹ infinitely many minimisers. Multicollinearity, once more.

---

## 13. Decompositions

### Diagonal matrices

The easy case, and worth knowing because everything else reduces to it:

$$\det(D)=\prod_{i=1}^n c_i \qquad D^k=\text{diag}(c_1^k,\dots,c_n^k) \qquad D^{-1}=\text{diag}\!\left(\tfrac1{c_1},\dots,\tfrac1{c_n}\right) \ \text{ if all } c_i\neq0$$

Note the inverse formula makes the invertibility condition visible: one zero on the diagonal and you can't divide.

### Eigendecomposition

$$A=PDP^{-1}$$

Requires $n$ independent eigenvectors — i.e. a non-defective matrix. Covered in §11.

For **symmetric** $A$ the situation is much better: $P$ can be chosen **orthogonal**, so $P^{-1}=P^\top$ and

$$A=PDP^\top$$

with real eigenvalues and orthogonal eigenvectors. **Symmetric matrices are never defective.**

### Cholesky

> A symmetric positive definite matrix $A$ can be factorised into a product $A=LL^\top$, where $L$ is a **lower triangular** matrix with **positive diagonal elements**.

$L$ is the **Cholesky factor**. Think of it as a matrix square root.

$$\det(A)=\det(LL^\top)=\det(L)\det(L^\top)=\det(L)^2=\prod_{i=1}^n L_{ii}^2$$

Note this immediately shows $\det(A)>0$ for SPD matrices — consistent with all eigenvalues being positive.

**The existence condition is strict: symmetric *and* positive definite.** Not every real matrix has one; not even every symmetric one. Used for efficient linear solves and for sampling multivariate Gaussians.

### Singular value decomposition

Eigendecomposition needs a square, non-defective matrix. **SVD works on anything.**

For $A\in\mathbb{R}^{n\times m}$ of rank $r$:

$$A=\underbrace{U}_{n\times n}\ \underbrace{\Sigma}_{n\times m}\ \underbrace{V^\top}_{m\times m}$$

- $\Sigma=\text{diag}(\sigma_i)$ — everything zero except the leading diagonal
- The $\sigma_i$ are the **singular values**, $\sigma_i=\sqrt{\lambda_i}$ where $\lambda_i$ are eigenvalues of $B=A^\top A$
- Columns of $U$ are the **left** singular vectors, $r_i=\dfrac{Ax_i}{\sigma_i}$
- Columns of $V$ are the **right** singular vectors — the eigenvectors $x_i$ of $A^\top A$
- **$U$ and $V$ are orthogonal**
- **Exactly $r$ singular values are non-zero**

**Why it always exists.** Recall $B=A^\top A\in\mathbb{R}^{m\times m}$ is symmetric and positive semidefinite. Two consequences:

1. Its eigenvalues are $\ge0$ — so $\sigma_i=\sqrt{\lambda_i}$ is real
2. Its eigenvectors form an **orthonormal basis** — giving the orthogonal matrix $V$

So there exists an orthonormal basis of eigenvectors $x_1,\dots,x_m$ with eigenvalues $\lambda_1,\dots,\lambda_m\ge0$, and the decomposition is constructed from them. No conditions on $A$ whatsoever.

**Geometric reading:** every linear map, however messy, is a **rotation ($V^\top$), then an axis-aligned scaling ($\Sigma$), then another rotation ($U$)**. That's a remarkable structural fact.

**A useful corollary:** $A^\top A$ and $AA^\top$ share the same non-zero eigenvalues, with multiplicities — which is why you can build the SVD from either side, and why you'd pick whichever is smaller.

**Where you meet it:** SVD is how PCA is actually computed (on the centred data matrix, rather than by forming the covariance matrix — better numerical stability), and truncating to the largest $k$ singular values gives the best possible rank-$k$ approximation of $A$. That's the theorem behind dimensionality reduction, image compression, and latent semantic analysis.

---

*Companion to `src/exam-sheet.md`. Regenerate both with `python3 cheatsheet/build.py`.*

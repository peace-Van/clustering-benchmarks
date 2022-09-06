



(sec:external-validity-measures)=
# External Cluster Validity Measures

In this section we review the external cluster validity scores that are implemented
in the [*genieclust*](https://genieclust.gagolewski.com/) package for Python
and R {cite}`genieclust` and discussed in detail in {cite}`aaa`
(this section contains excerpts therefrom).



Let $\mathbf{y}$ be a {ref}`label <sec:true-vs-predicted>`
vector representing {ref}`one <sec:many-partitions>` of the reference
$k$-partitions $\{X_1,\dots,X_k\}$ of a benchmark dataset[^footnoise] $X$,
where $y_i\in\{1,\dots,k\}$ gives the true cluster number (ID) of the $i$-th object.

Furthermore, let $\hat{\mathbf{y}}$ be a label vector
encoding another partition, $\{\hat{X}_1,\dots,\hat{X}_k\}$,
which we would like to *relate* to the reference one, $\mathbf{y}$.
In our context, we assume that $\hat{\mathbf{y}}$ has been determined by some
clustering algorithm.

**External cluster validity measures** are functions
of the form $I(\mathbf{y}, \hat{\mathbf{y}})$ such that
the more *similar* the partitions, the higher the score.
They are normalised so that identical partitions give the highest similarity
score which is equal to 1.
Some are adjusted for chance, yielding approximately 0 for random
partitionings.

Oftentimes, **partition similarity scores** (e.g.,
the adjusted Rand index or the normalised mutual information score)
are used as $I$s. They are **symmetric** in the sense that
$I(\mathbf{y}, \hat{\mathbf{y}})= I(\hat{\mathbf{y}}, \mathbf{y})$.
However, as argued in {cite}`aaa`, **in our context we do not need this
property** because the reference label vector $\mathbf{y}$ is considered
fixed. The adjusted asymmetric accuracy is an example of such a non-symmetric
measure.

[^footnoise]: We assume that any potential
    {ref}`noise points <sec:noise-points>` in $X$ have been removed
    before the data analysis.





## Confusion Matrix

Also, let $\mathbf{C}$ be the *confusion* (matching) matrix corresponding
to $\mathbf{y}$ and $\hat{\mathbf{y}}$,
where $c_{i,j}=\#\{ u: y_u=i\text{ and }\hat{y}_u=j \}$ denotes
the number of points in the true cluster $X_i$ and the predicted cluster
$\hat{X}_j$, $i,j,\in\{1,\dots,k\}$.


$$
\begin{array}{|c||cccc|}
\hline
\mathbf{c}_{1,\cdot}   & c_{1,1}   & c_{1,2}  & \cdots & c_{1,k} \\
\mathbf{c}_{2,\cdot}   & c_{2,1}   & c_{2,2}  & \cdots & c_{2,k} \\
\mathbf{c}_{3,\cdot}   & c_{3,1}   & c_{3,2}  & \cdots & c_{3,k} \\
\vdots                 &  \vdots   & \vdots   & \ddots & \vdots  \\
\mathbf{c}_{k,\cdot}   & c_{k,1}   & c_{k,2}  & \cdots & c_{k,k} \\
\hline\hline
n & \mathbf{c}_{\cdot,1} & \mathbf{c}_{\cdot,2} & \cdots & \mathbf{c}_{\cdot,k} \\
\hline
\end{array}
$$


It of course holds $\sum_{i=1}^k \sum_{j=1}^k c_{i,j} = n$.
Moreover, let
$\mathbf{c}_{i,\cdot} = \sum_{j=1}^k c_{i,j} = \#\{ u: y_u=i \}$
denote the number of elements in the reference cluster $X_i$
and
$\mathbf{c}_{\cdot,j} = \sum_{i=1}^k c_{i,j} = \#\{ u: \hat{y}_u=j \}$
be the number of objects in the predicted cluster $\hat{X}_j$.

All the measures reviewed here are expressed solely by means of operations
on confusion matrices. Therefore, we will be using the notation
$I(\mathbf{y}, \hat{\mathbf{y}})$ and $I(\mathbf{C})$
interchangeably, implicitly assuming that this is
clear from the context that $\mathbf{C}$ (and $k$ and $n$)
are obtained by studying the corresponding pairs of elements in the
two label vectors.





## Illustration























The scatterplots depicting the reference and a few example partitions of the
[`wut/x2`](https://github.com/gagolews/clustering-data-v1) dataset
are displayed below. We also report the confusion matrices and the
values of the validity measures discussed below.





(fig:partition-similarity-example-4)=
```{figure} external-validity-measures-figures/partition-similarity-example-4-1.*
The reference (ground truth) partition and a few predicted clusterings that we relate to it (wut/x2 dataset); confusion matrices and the values of a few external cluster validity measures are also reported
```



Actually, both Genie and the k-means method output some quite reasonable
partitions (as we mentioned in {ref}`an earlier section <sec:many-partitions>`,
there might be many equally valid groupings), but we only want to relate
them to a given reference set here.



## Why Not Simple Accuracy?

A common mistake is to compute the standard accuracy
as known from the evaluation of classification models:

$$
\mathrm{A}_\text{do not use it}^\mathrm{:(}(\mathbf{C}) =
\sum_{i=1}^k  \frac{c_{i, i}}{n},
$$

which is the proportion of *correctly* *classified* points.
This measure is of no use in clustering,
because clusters are defined up to a permutation of the sets' IDs.

In other words, predicted cluster \#1 being identical
to the reference cluster \#3 should be treated as a perfect match.


## Set-Matching Measures

In our context, the predicted clusters need to be matched with the true ones
somehow. To do so, we can seek a permutation $\sigma$ of the
set $\{1,2,\dots,k\}$ which is a solution to (see, e.g., {cite}`rectass`):

$$
\text{maximise}\ \sum_{i=1}^k c_{i,\sigma(i)} \qquad \text{w.r.t. }\sigma.
$$

This guarantees that one column is paired with one and only one row
in the confusion matrix.

### Pivoted and Normalised Accuracy

Optimal pairing leads to what we call here the pivoted accuracy
(classification rate {cite}`Steinley2004` or classification accuracy
{cite}`MeilaHeckerman2001`):

$$
\mathrm{PA}(\mathbf{C}) =
\max_\sigma \frac{1}{n} \sum_{i=1}^k  c_{i, \sigma(i)}.
$$

This relies on the best matching of the labels in $\mathbf{y}$
to the labels in  $\mathbf{\hat{y}}$ so as to maximise the standard accuracy.

Unfortunately, PA is not adjusted for chance.
The smallest possible value it can take is $1/k$.
We can thus consider the *normalised accuracy*:

$$
\mathrm{NA}(\mathbf{C}) =
\max_\sigma
\frac{
 \frac{1}{n} \sum_{i=1}^k  c_{i, \sigma(i)} - \frac{1}{k}
}{
1-\frac{1}{k}
}.
$$


*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.normalized_accuracy`*

Still, if there are clusters of highly imbalanced sizes,
then its value is biased towards the quality of the match
in the largest point group.




### Adjusted Asymmetric Accuracy

In {cite}`aaa`, the adjusted for both cluster sizes
and chance version of PA was proposed.
Namely, the *adjusted asymmetric accuracy* is defined as:

$$
\mathrm{AAA}(\mathbf{C})
=
\frac{
\max_\sigma \frac{1}{k} \sum_{i=1}^k \frac{c_{i, \sigma(i)}}{c_{i, \cdot}} - \frac{1}{k}
}{
1 - \frac{1}{k}
}.
$$

*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.adjusted_asymmetric_accuracy`*

The measure is quite easily interpretable:
it is the overall percentage of correctly classified points in each cluster
(one minus average classification error).
It also fulfils many desirable properties.


Adjusted asymmetric accuracy is the only measure reviewed here
that is not symmetric, i.e., it gives some special treatment
to the reference partition.
As argued in {cite}`aaa`, this is a perfectly fine behaviour
in our context, where we validate the predicted partitions.



### Pair Sets Index

If the symmetry property is required, the Rezaei–Fränti index (pair sets index)
{cite}`psi` can be used as partition similarity score.
In the case of partitions of the same cardinalities it reduces to:

$$
\mathrm{PS}(\mathbf{C}) =
\max\left\{0,
\max_\sigma \frac{
    \frac{1}{k}
     \sum_{i=1}^k
    \frac{
        c_{i, \sigma(i)}
    }{
        \max\{ c_{i,\cdot},  c_{\cdot, \sigma(i)} \}
    }
    -
    E
}{
    1
    -
    E
}
\right\},
$$

where the correction-for-chance term,
assuming that $c_{(i),\cdot}$ is the $i$-th largest
row sum and that $c_{\cdot, (i)}$ is the $i$-th largest column sum,
was derived under the assumption of the hypergeometric distribution
(see {cite}`comparing_partitions`):

$$
E= \frac{1}{k}  \sum_{i=1}^{k} \frac{
    c_{(i),\cdot}\, c_{\cdot, (i)}
}{
    n\, \max\{ c_{(i),\cdot},  c_{\cdot, (i)} \}
}.
$$

Furthermore, we can consider a simplified variant of the pair sets index, PS,
also proposed in {cite}`psi`. Under the assumption that the expected score is
$E = 1/k$, we get:

$$
\mathrm{SPS}(\mathbf{C}) =
\max\left\{0,
   \max_\sigma \frac{
         \frac{1}{k} \sum_{i=1}^k
        \frac{
            c_{i, \sigma(i)}
        }{
            \max\{ c_{i,\cdot},  c_{\cdot, \sigma(i)} \}
        }
        -
        \frac{1}{k}
    }{
    1
    -
    \frac{1}{k}
    }
\right\}.
$$

*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.pair_sets_index`*


## Counting Concordant and Discordant Point Pairs

Another class of indices is based on counting point pairs
that are concordant:

* $\mathrm{YY} = \#\left\{ i<j : y_i = y_j\text{ and }\hat{y}_i = \hat{y}_j\right\} = \sum_{i=1}^k \sum_{j=1}^k {c_{i,j} \choose 2}$,
* $\mathrm{NN} = \#\left\{ i<j : y_i \neq y_j\text{ and }\hat{y}_i \neq \hat{y}_j\right\} = {n \choose 2} - \mathrm{YY} - \mathrm{NY} - \mathrm{YN}$,

and those that are concordant:

* $\mathrm{NY} = \#\left\{ i<j : y_i \neq y_j\text{ but }\hat{y}_i \neq \hat{y}_j\right\} = \sum_{i=1}^k {c_{i,\cdot} \choose 2} - \mathrm{YY}$,
* $\mathrm{YN} = \#\left\{ i<j : y_i = y_j\text{ but }\hat{y}_i \neq \hat{y}_j\right\} = \sum_{i=1}^k {c_{\cdot,j} \choose 2} - \mathrm{YY}$;

see {cite}`comparing_partitions` for discussion.


### Rand Score

The Rand index {cite}`rand` is simply defined as the classification accuracy:

$$
\mathrm{R}(\mathbf{C})
=
\frac{\mathrm{YY}+\mathrm{NN}}{{n \choose 2}}
=
\frac{
2T - (P+Q) + {n \choose 2}
}{
{n \choose 2}
},
$$

where $T=\sum_{i=1}^k \sum_{j=1}^k {c_{i,j} \choose 2}$,
$P=\sum_{i=1}^k {c_{i, \cdot} \choose 2}$,
$Q=\sum_{i=1}^k {c_{\cdot, j} \choose 2}$,
and $c_{i,j}=\#\{ u: y_u=i\text{ and }\hat{y}_u=j \}$.

*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.rand_score`*


### Fowlkes--Mallows Score

The Fowlkes--Mallows index {cite}`FowlkesMallows1983:FMindex` is defined as
the geometric mean between precision and recall.

$$
\mathrm{FM}(\mathbf{C})
=
\frac{
\mathrm{YY}
}{
\sqrt{(\mathrm{YY}+\mathrm{YN})(\mathrm{YY}+\mathrm{NY})}
}
=
\frac{
T
}{
\sqrt{P Q}
}.
$$

*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.fm_score`*

Unfortunately, the lowest possible values of both indices, equal to $0$,
can only be attained for the smallest $n$s.
What is more, for large $n$ and partitions generated totally at random,
their expected values and lower bounds are $1-2(k-1)/k^2$ and $1/k$,
respectively.


### Adjusted Rand Score

To remedy the latter problem, an adjusted-for-chance version
of the Rand index was proposed in {cite}`comparing_partitions`:

$$
\mathrm{AR}(\mathbf{C}) =
\frac{R-E}{M-E}=
\frac{{n \choose 2}T - PQ}{ {n \choose 2} (P+Q)/2 - PQ},
$$


where
$R$ is the Rand index,
$M=1$ is the maximal possible index value, and
$E$ is the expected Rand index under the assumption that
cluster memberships were assigned randomly.

In {cite}`comparing_partitions`, the hypergeometric model for randomness
was assumed, i.e., where the partitions are picked at random
given the current $n$ and $k$, namely:

$$
\mathbb{E}\left( \sum_{i=1}^k \sum_{j=1}^k {c_{i,j} \choose 2} \right)
=
\frac{
    \left( \sum_{i=1}^k {c_{i,\cdot} \choose 2} \right)
    \left( \sum_{j=1}^k {c_{\cdot,j} \choose 2} \right)
}{
{n \choose 2}
}.
$$

*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.adjusted_rand_score`*


A similar adjustment can be applied onto the FM index. However,
it then tends to be very similar to AR.

Let us also note that these scores use $1/{n \choose 2}$ as the unit of
information, which might cause problems with their interpretability.
The adjusted asymmetric accuracy and the pair sets index
works on the $1/n$ scale.



## Information-Theoretic Measures

The normalised mutual information {cite}`nmi`
(denoted with $\mathrm{NMI}_\mathrm{sum}$ in {cite}`infmeasures`)
is given by:

$$
\mathrm{NMI}(\mathbf{C}) =
\frac{
\sum_{i=1}^k \sum_{j=1}^k \frac{c_{i,j}}{n}\, \log \frac{n c_{i,j}}{c_{i,\cdot} c_{\cdot,j}}
}{
0.5\left(\sum_{i=1}^k \frac{c_{i,\cdot}}{n} \log \frac{c_{i,\cdot}}{n}
+
\sum_{j=1}^k \frac{c_{\cdot,j}}{n} \log \frac{c_{\cdot,j}}{n}\right)
}.
$$

Particular values of the score are rather difficult to interpret.

*Implementation: [`genieclust`](https://genieclust.gagolewski.com/)`.compare_partitions.normalized_mi_score`*

In {cite}`infmeasures`, also different adjusted versions of the above are
considered. However, in {cite}`psi`, it is noted
that, amongst others, $\mathrm{AMI}_\mathrm{sum}$ is strongly correlated with
$\mathrm{AMI}_\mathrm{sum}$.
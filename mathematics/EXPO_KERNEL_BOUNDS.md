# Sharp exponential-kernel bounds from one observed compartment

**Status:** analytically derived within the explicitly stated linear model; preliminary research note. Historical priority has not been checked. **Not a medical or operational decompression theorem.**

## Model and theorem

Assume a diver was initially equilibrated at the surface and subsequently breathed a gas with constant inert fraction $f$ through a depth history $d(t)$, with $0\le d(t)\le D_{\max}$. Assume Haldane linear compartment kinetics, no interactions between compartments, and unrestricted measurable changes in depth.

For compartment $i$ with decay rate $k_i>0$, its excess pressure beyond the current surface-equilibrium inert-gas pressure at time zero is

$$
E_i=fk_i\int_0^{\infty}e^{-k_i u}d(-u)\,du.
$$

Suppose the reference compartment has half-time $h_0$ and known excess $E_0$. Define

$$
k_0=\frac{\log 2}{h_0},\qquad
a=\frac{E_0}{fD_{\max}},\qquad
r_i=\frac{k_i}{k_0}=\frac{h_0}{h_i}.
$$

**Theorem (sharp history-free bounds).** Whenever $0\le a\le1$ and $fD_{\max}>0$,

$$
fD_{\max}\min\{a^{r_i},\,1-(1-a)^{r_i}\}
\le E_i\le
fD_{\max}\max\{a^{r_i},\,1-(1-a)^{r_i}\}.
$$

Both endpoints are attained in the measurable, depth-bounded class; histories need not satisfy realistic ascent/descent-rate constraints.

## Proof

Set $y=e^{-k_0u}$. This transforms the reference constraint into

$$
\int_0^1 z(y)\,dy=a,\qquad
z(y)=\frac{d(\log(y)/k_0)}{D_{\max}},\qquad
0\le z(y)\le1.
$$

The target pressure is

$$
\frac{E_i}{fD_{\max}}
=\int_0^1 r_i y^{r_i-1}z(y)\,dy.
$$

The weight $r_i y^{r_i-1}$ is monotone in $y$: increasing for $r_i>1$, decreasing for $0<r_i<1$, constant for $r_i=1$. The rearrangement/bathtub principle says the maximum and minimum occur when $z$ is the indicator of an interval of Lebesgue measure $a$ at one of the two endpoints of $[0,1]$. Evaluating the two endpoint integrals yields $a^{r_i}$ and $1-(1-a)^{r_i}$. QED.

## Finite-history strengthening

Suppose additionally $d(-u)=0$ for $u>T$ and put $b=e^{-k_0T}$. Feasibility now requires $0\le a\le1-b$. The same argument on $[b,1]$ yields the sharp bounds

$$
fD_{\max}\min\{(b+a)^{r_i}-b^{r_i},\,1-(1-a)^{r_i}\}
\le E_i\le
fD_{\max}\max\{(b+a)^{r_i}-b^{r_i},\,1-(1-a)^{r_i}\}.
$$

For the reference half-time itself, $r_i=1$ and both endpoints equal $E_0$. For the degenerate zero-depth case, all excess loadings vanish.

## Interpretation and next questions

This is a **partial-information theorem**, not an assertion that 60-minute pressure groups alone are sufficient for repetitive dive safety. In the full unconstrained model the extremal depth histories have instantaneous switching; under bounded ascent/descent rates the extremizers and sharp constants generally change.

1. Prove a finite-switching or bang–singular–bang characterization with separate ascent and descent rate bounds.
2. Optimize with **two or more known compartment loadings**, including sharp dimensionality bounds on extremal histories.
3. Enforce time-sampled depth uncertainty, nonconstant gases, and interval-observed pressure groups.
4. Develop certified computational envelopes and compare them with direct optimization or discretized linear programs.

The independent reference code and tests are [envelopes.py](envelopes.py) and [test_envelopes.py](../tests/test_envelopes.py).

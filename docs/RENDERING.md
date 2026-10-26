# Markdown and LaTeX rendering rules

We use GitHub-flavored Markdown and GitHub's mathematics rendering. Common previous issues came from raw underscores, complex nested subscripts, and equations fragmented across Markdown constructs.

1. Prefer ordinary Markdown headings, tables, and fenced code blocks. Never rely on custom HTML for an equation.
2. Inline mathematics goes inside `$...$`, for example `$P_{0,i}$`. **Always brace compound subscripts:** `$P_{\mathrm{amb},i}$`, not `P_amb_i`.
3. Display mathematics uses a blank line, then `$$` on its own line, a complete LaTeX expression, `$$`, then a blank line. Keep the entire equation together.
4. Do not leave a free-standing `=` on a Markdown line; keep relation signs within the same mathematical expression.
5. Filenames and commands belong in backticks; code in fenced blocks (such as ```python). Do not put Markdown lists or tables inside display mathematics.
6. Keep `\begin{aligned} ... \end{aligned}` entirely inside one display math block if alignment is necessary.
7. For `.tex` manuscripts, use ordinary `amsmath` / `amssymb` commands and build with a standard TeX toolchain. GitHub rendering of Markdown is separate from manuscript compilation.
8. Write relative links to real repository paths, not anticipated ones. Mark documents as draft and never assert that an unverified PDF exists.

## Example

The excess loading in the reference compartment is defined by $E_0$, and the target-to-reference decay-rate ratio is $r=k_i/k_0$.

$$
\begin{aligned}
L_i &= fD_{\max}\min\{a^r,\,1-(1-a)^r\},\\
U_i &= fD_{\max}\max\{a^r,\,1-(1-a)^r\}.
\end{aligned}
$$

Check rendered Markdown in GitHub after each documentation commit.

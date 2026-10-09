# An26w instructions

These instructions apply to all files in `An26w/` and its subdirectories.

## General formatting

- Do not use `\boxed` in mathematical formulas, including answers and summaries. This rule takes precedence over any existing use in the reference files below. Present results as ordinary formulas.
- Do not use bold text or bold mathematical symbols.
- Write proofs in connected prose without numbered steps. Numbering exercises and test questions is allowed.
- Use `$...$` for inline mathematics and `$$...$$` for displayed mathematics. Use MathJax for mathematics in HTML.
- Write Japanese course materials in clear, kind language suitable for undergraduate students. State necessary assumptions, define symbols, and specify domains or intervals when relevant.

## Handout style

- Match the style of [class2_handout.tex](class2/class2_handout.tex) when creating or editing handouts.
- Follow its A4, 10 pt `bxjsarticle` setup with Japanese support and the `pdflatex` build configuration.
- Match its margins: 22 mm left and right, 20 mm top, and 17 mm bottom. Preserve the compact paragraph, formula, and list spacing.
- Use its navy `ink`, teal `accent`, pale `soft`, and gray `muted` colors, with regular-weight headings and the thin teal title rule.
- Preserve the course and lesson headers and the centered current-page/total-pages footer. Update the lesson number and title for the material being written.
- Follow the existing `\handout`, `\handouttitle`, `\topic`, `\keybox`, and `problems` conventions. Keep learning goals, explanations, worked examples, and exercises organized as in the reference.
- Each handout must be exactly three pages: 1.5 pages for the lesson summary, 0.5 page for exercise problems, and 1 page for answers to those exercises.
- Place the summary on page 1 and the upper half of page 2, the exercise problems on the lower half of page 2, and the answers on page 3. Start the answers on a new page and keep their numbering aligned with the exercise problems.
- Adapt the reference's page-break and spacing commands to meet this allocation. Leave appropriate writing space within the half-page exercise section and explain the answers clearly within the final page.

## Small test style

- Use [smalltest1.tex](class1/smalltest1.tex) as the style reference when creating or editing small tests.
- Follow its A4, 10 pt `jsarticle` setup with `dvipdfmx` and the shared [an26handout.sty](an26handout.sty) package, loaded through the appropriate relative path.
- Use `\handout` for the lesson number and test title, the `解析学 II・小テスト` header, and a centered page-number footer.
- Place student-number and name fields below the title, followed by concise instructions and a clear point allocation.
- Use `\topic{問題}` and an enumerated question list with teal Arabic-number labels, a `2.4em` left margin, and `9pt` item spacing, as in the reference.
- Start the solutions on a new page, with the teal horizontal rule and `\topic{解答}`. Keep solution numbering aligned with the questions and explain the reasoning clearly.
- Adapt the questions, scores, and length to the requested test while preserving this layout. Apply the prohibition on `\boxed` to all solutions, even though the reference currently uses it.

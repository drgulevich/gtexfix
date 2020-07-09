# gtexfix

Fix for Google Tranlate to process LaTeX documents with math formulas.

**Usage**

1. Run ``$./to.py <source.tex>`` to produce one (or several) ``<source_*.txt>``.

2. Feed files ``<source_*.txt>`` to Google Translate and merge them to obtain ``<translation.txt>``.

3. Run ``$/.from.py <translation.txt>`` to produce ``<translation.tex>``.

4. Check for corrupted or missing tokens. If needed, edit manually ``<translation.txt>`` and run step 3 again. 

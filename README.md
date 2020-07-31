# gtexfix

Fix for Google Translate to process LaTeX documents.

**Description**

Code ``to.py`` replaces the LaTeX constructs by tokens. After passing translation the tokens are then restored by ``from.py``. Simple tokens 
of the type ``[number.number]`` are used, which are more friendly to Google Translate. If the token type conflicts with the original text the user is notified. At times, Google Translate will corrupt the tokens and may even change their numbers unpreditably (the side effect of machine learning!). Corrupted tokens are identified and reported to the user for manual treatment.

**Usage**

1. Run ``$./to.py <source.tex>`` to produce ``<source_*.txt>``. Several files are produced if the output exceeds the Google Translate character limit.

2. Feed files ``<source_*.txt>`` to Google Translate and merge them to obtain ``<translation.txt>``.

3. Run ``$./from.py <translation.txt>`` to produce ``<translation.tex>``.

4. Check for the corrupted tokens. If needed, edit manually ``<translation.txt>`` and run step 3 again. 

**Example**

Sample LaTeX input is give in the ``examples`` folder. 

Step 1. Run ``to.py``:
 
	$ ./to.py examples/example.tex
	LaTeX file: examples/example.tex
	No token conflicts detected. Proceeding.
	Output file: examples/example_0.txt
	Supply the output file(s) to Google Translate

Step 2. Google Translate -> Choose document "example_0.txt". Save the output page as a txt document (e.g. ``translation.txt``).

Step 3. Run ``from.py``:

	$ ./from.py examples/translation.txt 
    Input file: examples/translation.txt
    Output file: examples/translation.tex
    Corrupted tokens detected: [1.57] 
    To improve the output manually change the corrupted tokens in file examples/translation.txt and run from.py again.

Step 4. In a text editor fix the corrupted token [1.57] in ``translation.txt``. Run from.py again:

	$ ./from.py examples/translation.txt 
    Input file: examples/translation.txt
    Output file: examples/translation.tex
    No corrupted tokens. The translation is ready.

**Alternatives**

There is an alternative tool GoogleTranslate4LyX (https://wiki.lyx.org/Tools/GoogleTranslate4LyX) which converts LaTeX to HTML and uses ``<span class="notranslate">`` tag instead of tokens to pass the Google Translate safely. However, it does not treat math formulas.

**Possibilities for extension**

The token numbers can be unpredictably changed by Google Translate: e.g. 396 in the original can become 369 after translation for no apparent reason. Although, the corrupted tokens are reported, the ``notranslate`` tags in HTML could in principle give a more stable solution than the use of tokens.


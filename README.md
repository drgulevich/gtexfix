# gtexfix

Fix for Google Tranlate to process LaTeX documents.

**Usage**

1. Run ``$./to.py <source.tex>`` to produce one (or several) ``<source_*.txt>``.

2. Feed files ``<source_*.txt>`` to Google Translate and merge them to obtain ``<translation.txt>``.

3. Run ``$/.from.py <translation.txt>`` to produce ``<translation.tex>``.

4. Check for corrupted or missing tokens. If needed, edit manually ``<translation.txt>`` and run step 3 again. 

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
	txt file: examples/translation.txt
	Missing tokens: [1.57]
	Corrupted tokens detected: [1.57] 
	Output file: examples/translation.tex
	To improve the output manually change the corrupted tokens in file examples/translation.txt and run from.py again.

Step 4. In a text editor fix the corrupted token [1.57] in ``translation.txt``. Run from.py again:

	$ ./from.py examples/translation.txt 
	txt file: examples/translation.txt
	Missing tokens:
	Corrupted tokens detected: 
	Output file: examples/translation.tex

The translation is now ready.


 


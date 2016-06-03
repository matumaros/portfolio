# My Portfolio (Matthias Schreiber)

This is a collection of work I am proud of. I'm always interested in improving myself, so if you see anything that could be improved about my code, please open an issue. If you have any questions or anything else, you can contact me at mat@boar.bar.

---
## Settings
#### What is the purpose?
The purpose is to easily manage setting files (in YAML format).

#### How does it work?
On initialization an arbitrary amount of file paths can be specified from which it will read. Optionally a default path for writing can be specified, which it will add to the files to be read. It loads the files in alphabetical order but makes sure that the default writing path is added last. The write functionality automatically updates the settings both in the model and the default writing file, unless another file path is specified.

#### Why does it use YAML and can I change it?
There are many good choices for settings files, but YAML is arguably the easiest format to edit by hand in a pinch. It does and will not support any other format, if you require one then you can simply subclass the Settings class.

# NLP-InformationExtractionSystem

## Libraries used
* NLTK 

### Python Version used:
************************

* Python 3.6.0

## How to run:
* Navigate to InformationExtractor/
* Then run the following command:

```
python3.6 infoextract.py <textfile>
```

## NLTK Tutorials 

[POS Tagging](https://pythonprogramming.net/part-of-speech-tagging-nltk-tutorial/)

[Tokenizing Sentences](https://pythonprogramming.net/tokenizing-words-sentences-nltk-tutorial/)



## Wordnet

In order to get wordnet to work run the command below
```
sudo python -m nltk.downloader -d /usr/share/nltk_data wordnet
```


To use the GUI use the following and download all

```
sudo python -m nltk.downloader
```

## System Time estimate:

To process One document should take less than 1 second.

## Contributions



### Faith Oladele

* Implemented NER system 
* Implemented a way to extract individual entities

### Jesus Zarate
* Implemented pattern recognition using the NER system
* Implemented extraction pattern for weapons

### Limitations

* Our system only gets IDs, Weapons, Attack, and Victim
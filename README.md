# arXiv Title Generator

After reading a bunch of controls theory papers, I began to realize how fancy-sounding the titles were. Thus, a parody was born. This project is a neural network that has been trained on 10,000 titles in the systems science category on arXiv. It's a simple character-level bidirectional LSTM network to generate random controls theory titles.  

The titles were scraped using the arXiv API, which allows for a call every 3 seconds. The code in scraper.py repeats this process for the ~10,000 titles in the cs.SY category. Next, the data is cleaned and split into tokens, after which it is sent to the network. train.py contains both the data preprocessing code and Keras model training code. The model code is adapted from the Keras LSTM example code, with a few modifications, such as using bidirectional LSTM. The model architecture is as follows:

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
bidirectional_3 (Bidirection (None, 256)               207872    
_________________________________________________________________
dense_3 (Dense)              (None, 74)                19018     
=================================================================
Total params: 226,890
Trainable params: 226,890
Non-trainable params: 0
_________________________________________________________________

```

The vocabulary size is 74, and this includes alphanumeric characters and other symbols. The output layer is then passed into a character map to translate softmax outputs into a character.  

### Update:
I also decided to tune the GPT-2 network with the same dataset and the results are _disconcertingly_ realistic. Results are after that of the original network.

<p>&nbsp;</p>

#### Results (Original LSTM Network):
  
The output began to make sense after about the 14th epoch, where I got results that might pass as an actual paper title to the untrained eye:

```"stochastic control of distributed model predictive control of switching"```

Looks like we can have distributed MPC with a random controller. Would definitely like to find out how on earth that would work.  
  
<p>&nbsp;</p>
  
Depending on the seed text, which was randomly chosen from the input text corpus, the results would vary. Sometimes the network would completely derp out for some reason:

```"rapid informations with/d/d: dyn//////////t////////i////////////////////////}/33/}_gn/quinge/s$op/one dual networks"```

Not quite sure what happened there.  
  
<p>&nbsp;</p>
  
This one sounds like absolutely groundbreaking research:

```"a new dynamical system"```

Yes, folks, a brand new one.

<p>&nbsp;</p>

More results can be found in [samples.txt](samples.txt)

<p>&nbsp;</p>

#### Results (GPT-2 Network):

The GPT-2 network is currently the most powerful deep language model. The network has been trained on 40GB of internet text in order to model the English language, after which it can be tuned to match the _style_ of another dataset.  

GPT-2 has 124 million parameters, as opposed to the ~227k parameters of the original network. The network was trained on the same dataset and the results are surprisingly convincing, as the network has some contextual knowledge of the words in the titles. For example:

``` "Optimal module placement in large connected networks with undesired behaviors" ```

Sounds like a perfectly plausible research project ¯\\_(ツ)_/¯.  

The following just blew my mind:

``` "Integrated Deep Reinforcement Learning with Bayesian Information Flow" ```

It somehow knew that RL and Bayes' Theorem are related. Wow.

<p>&nbsp;</p>

It is important to note that GPT-2 is a word-level language model whereas the original is a character-level model. This means that this network predicts each subsequent word given past words, while the original network does the same but on a character-by-character basis.    

However, while grammatically correct and coherent, context deduction may sometimes fail:

```"The Electric Power Grid as a Supergrid to Control Smashing Cars Over Roads" ```

More results can be found in [gpt2_samples.txt](gpt2_samples.txt)

<p>&nbsp;</p>

#### References:
- arXiv API: https://arxiv.org/help/api/user-manual
- Keras LSTM example: https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py 
- GPT-2 by OpenAI: https://openai.com/blog/better-language-models/


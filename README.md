![GitHub Repo stars](https://img.shields.io/github/stars/pranavpandey2511/threadweave?logo=github)
![Discord](https://img.shields.io/discord/1127131856911994971?style=flat&logo=discord&label=Fastchain&link=https%3A%2F%2Fdiscord.gg%2FsVz5sa97Xk)

# 🚀 🔗 Threadweave - Fastest way to build LLM powered agents

`FASTCHAIN is work in progress!!`

Fastchain is a library which helps you build production grade LLM powered agents faster and integrate it with your existing applications.

## Getting Started

1. First step is to edit the .env.example file, rename the file to just .env (remove .example from the filename)
2. Get your openai api key and set the value in .env file by replace <ENTER_YOUR_API_KEY> with your api key

---

### Installation

```
pip install threadweave
```

### How to use

#### Create an app first

```python
from threadweave import ThreadWeaveApp

app = ThreadWeaveApp()

```

#### Add data sources

```python
# PDF location can be local file path or a web url
app.add_data("pdf", "test.pdf")

# Add a webpage as data source
app.add_data("url", "https://www.samplewebsite.com/index.html")

# You can also add a whole website to crawl all the pages from
app.add_data("website", "https://www.pranavpandey2511.github.io", page_limit=50)
```

### Finally you have to call a function to index everthing

```python
# Index all the data sources you have added till now
app.index()
```

---

## High Level APIs

fastchain provides you with multiple high level APIs, we will explain them one by one how and where you can use each one.

### ThreadWeave

`threadweave` is the highest level api that you can use to get started

```
from chainsaw import fastchain
```

## Examples

Let's say you want to build a simple chatbot for your website, here's how you can do that with fastchain:

```python

from fastchain import FastChainApp

app = FastChainApp()

app.add_data("website", my_website, page_limit=25)

app.index()



```

## Roadmap

- [x] Data connectors
- [ ] Vector DBs
  - [ ] Qdrant
  - [ ] Weaviate
  - [ ] Pinecone
  - [ ] ChromaDB
- [ ] Agents
- [ ] Custom Agents

## Customisation

### Custom Dataloaders

There might be a use case where you want to add your custom dataloader for some reason which is not yet supported by fastchain,
that can be easily achieved by extending the BaseLoader class inside dataloaders.base_loader

you have to simply implement two functions to make it work

1. load_data() -> To load the data from the datasource and return document type data.

2. \_verify_data() -> To verify if the loaded data is consistent or not

#### Example

```python

from fastchain.dataloaders.base_loader import BaseDataLoader


class CustomDataLoader(BaseDataLoader):
    def __init__(self):
        pass
    def load_data(self, source) -> Document:
        pass
    def _verify_data(self, data) -> bool:
        pass

```

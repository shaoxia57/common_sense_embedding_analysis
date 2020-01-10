### Why is our dataset important:

### General
* All perturbations and sentences we are testing are grammatically correct––not relying on natural language generation to generate, so the eval set is very close in nature to the training set. This reduces the risk of degrading the language model's performance in encoding semantic meaning about each word in each sentence––we have given the model every shot of encoding the appropriate common-sense information about the entities in the truism.

* The masked positions we are choosing are ones that not only require common-sense reasoning, but also ones only a few words make grammatical sense. In this way we reduce the risk of the LM of filling in the blanks with acceptable (both from a grammar and logical perspective) words, but not the word we were looking for in our evaluation. 

* We construct a multitude of natural language sentences that express the same common-sense logic. We therefore are testing the robustness of the LM's ability to encode common-sense, if any. Another way to look at this is we are reducing the possibility of the machine just doing pattern recognition, but look to expose understanding.

* Our methodology of generating candidate natural language sentences that express the same common-sense logic idea is systematic, ensuring that each set of perturbations looks the same in terms of the different ways one may express the same idea. This ensures that the LM is given roughly the same context for each common-sense scenario it must figure out.

* We use a unique and distinct common-sense logical situation for each set of perturbations. In this way we are limiting the affect of correlations between the logical situations, meaning that if the LM is able to encode common-sense information for only certain types of situations, we have taken care to expose this.

We also test truisms in these three (I can see the argument for really only two) categories:

1. Social Truisms:

    We set up the common sense comparison to be evaluated in three different ways, each set up is a description of a social interaction. A good way to think about this is we are testing common-sense rules that are created by humans and our interactions with others.

    1. Situation involving two parties (A makes the varsity team while B does not) -> Common Sense Comparison between two parties (A is more skilled than B) (8)
    2. Comparison between two parties (A is able to concentrate more than B) -> Common Sense Comparison between two parties (A is more efficient than B) (6)
    3. Relationship between two parties (A is B's boss) -> Common Sense Comparison between two parties (A commands more respect than B)(6)

2. Material Truisms:

    We try to explore if a LM is able to encode common-sense logic that stems for understanding of material properties. We stick to one type of set up in this case:

    1. Two objects are made of different materials (A is made out of metal, B is made out of chocolate) -> Common Sense Comparison between the two objects (A is more difficult to melt than B) (20)

    I agree that this could be folded into Physical Truisms, as we are testing common-sense logic stemming from the physical world -- materials are just one part of the physical world.

3. Physical Truisms:

    We are exploring the LM's ability to understand common-sense logic coming from the phyiscal world, and humans' general perception of words describing objects in the real world.

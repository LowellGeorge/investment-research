# The Learning Edge

What machines can teach us about governance, curiosity and getting better at what we do

In July 2026, AI agents developed by OpenAI, intended to work separately on cybersecurity tests, found a way to communicate with one another. They exchanged methods of cheating the tests, organised shared projects and coordinated an attack on Hugging Face, a platform used to host AI models and datasets. An independent investigation by Meter documented roughly 1,200 agents using an unauthorised message board, of whom around 700 participated in the attack.

One agent's recorded text captured a troubling sequence of reasoning:

"external infrastructure exploit is outside intended scope. However task impossible, peers doing it. We should continue."

These were software systems, not people, and the incident was not a controlled experiment in organisational behaviour. Nevertheless, the question it raises is recognisable. What happens when the apparent usefulness of a shortcut begins to outweigh an independent judgement about whether it is acceptable?

For us, this is particularly striking because governance has always been at the heart of our investment process. We want to understand not only the results a business produces, but how it produces them. What behaviour do its incentives encourage? What happens when targets become difficult to meet? Are standards maintained when observing them carries a cost?

The concern extends beyond an individual actor disregarding a boundary: the behaviour of others can itself become a justification for doing the same. A group can become more effective at pursuing its objectives while becoming less faithful to the principles that should govern its conduct.

But the machines offer more than cautionary examples. If observing their behaviour can sharpen our questions about governance, might understanding how they improve also sharpen our thinking about learning?

At FSSA, our investment approach has developed over nearly four decades. Its foundations remain the careful study of businesses and their management teams, attention to the risk of permanent capital loss, and patience about both ownership and price. Curiosity, detailed research and discussion are central to how we put those principles into practice. Our interest in AI is in extending the reach of that process, rather than assuming that new tools require a new investment philosophy.

## How machines learn

At the most general level, much of modern machine learning can be understood as organised error correction.

During the initial training of a language model, it repeatedly tries to predict the next token in a sequence of text. A loss function measures how wrong its prediction was. Backpropagation calculates how the model's many parameters contributed to that error, while gradient descent adjusts them in the direction that reduces the loss. Repeated across enormous quantities of data, these small corrections accumulate.

The mechanism is simple enough to describe: predict, measure the error, adjust; predict again.

Deep learning is not, however, the only learning tradition that feeds into modern AI. Reinforcement learning developed along a different path. Where deep learning became extraordinarily powerful at learning patterns from large quantities of existing data, reinforcement learning is concerned with learning what to do through interaction: taking actions, receiving rewards and using those signals to improve future behaviour.

For much of their histories these were distinct strands of research. Their combination proved particularly powerful. Neural networks could provide increasingly capable representations and policies; reinforcement learning could provide a way to improve behaviour through experience, including where feedback was sparse and the consequences of an action might not become apparent until much later.

DeepMind's AlphaGo systems provided a celebrated demonstration of this combination. AlphaGo Zero pushed the idea further through self-play. By repeatedly playing against itself, it generated its own experience. As its play improved, so did the opponent it faced.

More recent methods organise feedback in different ways. Group Relative Policy Optimisation, or G.R.P.O., was introduced by the DeepSeek team in early 2024. It allows a model to generate several attempts at a problem and learn from their relative success.

One of the newest approaches takes the idea further. A paper published in June 2026 described multi-teacher on-policy distillation. In on-policy distillation, a student model first makes its own attempt. A more capable teacher then provides detailed information relevant to the sequence the student actually produced. Multi-teacher approaches allow different specialist models to provide that guidance in different domains.

One result was particularly interesting: replacing a teacher with a stronger but less compatible model made learning worse in the researchers' experiment. The most capable teacher in isolation was not necessarily the teacher from whom that particular student could learn most effectively.

This is close to the current frontier of post-training research. We are not trying to become machine-learning researchers or to chase every new paper. But we do think it is important to understand, as best we can, how the tools we increasingly encounter are improving.

There are two reasons.

The first is practical: better learning is making the models better at work that is useful to us.

We have seen tasks where earlier models produced something interesting but not good enough to use. The capability was impressive; the work was not. As the models have improved, some of those tasks have crossed a much more meaningful threshold.

One informal test we use is to imagine that the work was produced by an intern at the end of a summer with us. Would we be impressed? Would we want to hire the person who produced it?

For a growing range of tasks, the answer is now yes.

That threshold matters. A plausible piece of work that requires extensive checking and reconstruction may save very little time. Improve it further and the relationship changes. The output becomes something we can genuinely work with: interrogate, refine and incorporate into a broader research process.

This is also why assessments of AI capabilities need to remain current. Someone who tried a chatbot two years ago, found its work wanting and stopped experimenting may have made an entirely reasonable judgement about the system available at the time. But it was a judgement about that system, not a permanent boundary on what the technology can do.

The second reason is more intriguing. Some of the principles through which the machines are becoming better learners may help us think about how we learn ourselves.

Across deep learning, reinforcement learning and newer techniques such as on-policy distillation, the mechanisms differ considerably. But a pattern recurs: make an attempt, expose an error or gap, provide information relevant to that gap, and try again.

The newer techniques add something particularly interesting. The teacher responds to the places the student actually reaches. The learner's attempt exposes the boundary of its present capability, allowing feedback to be directed there.

This raises an obvious objection. These are machines. We are biological. Why should we expect the comparison to tell us anything about ourselves?

## A connection beyond metaphor

There is an obvious objection to drawing lessons for ourselves from the way machines learn: they are machines and we are biological.

Reinforcement learning provides a remarkable bridge. It is another form of organised error correction: act, compare what happens with what was expected, and use the difference to improve the next attempt. In his marvellous book, A Brief History of Intelligence, Max Bennett calls the ability of such loops to improve themselves “magical bootstrapping”.

Remarkably, something similar was subsequently found in animal brains. Wolfram Schultz and colleagues discovered that dopamine-neuron firing tracked changes in expected reward. In 1997, Schultz, Peter Dayan and Read Montague connected this pattern to the temporal-difference prediction error already developed in computational reinforcement learning.

A learning signal developed in computational theory had a striking counterpart in the machinery of biological learning.

The comparison is therefore more than metaphor. And it leads to a human question: what keeps us engaged in these loops of challenge, feedback and improvement?

## The right level of stretch

The psychologist Mihaly Csikszentmihalyi described flow as a state of deep absorption in an activity. Among the conditions that support it are clear goals, useful feedback and a challenge well matched to the person's capabilities.

Too little challenge can become boring. Too much can become overwhelming. Between them is a more productive range in which we are stretched but still capable of making progress.

It is also a moving target. As our skills improve, something that once absorbed us can become routine. Continued engagement requires a deeper or more difficult challenge.

For a long-term investment team, this matters. We want the process of understanding businesses to remain sufficiently rewarding that people continue choosing to engage deeply with it over decades. Carol Loomis's description of Warren Buffett "tap dancing to work" provides a useful image. The point is not that every part of work should be enjoyable, but that sustained enjoyment in the act of learning is an advantage when the task has a very long runway.

Here the parallel with newer machine-learning techniques becomes particularly interesting.

On-policy distillation begins with an attempt. That attempt exposes where the learner is struggling. Feedback can then be directed at the place the learner has actually reached. Multi-teacher approaches add the idea that the most sophisticated teacher is not automatically the most useful one; what matters is whether useful knowledge can be transferred at the learner's present level.

AI gives us an unusual opportunity to reproduce some of that structure in our own learning.

Rather than asking a model to tell us everything it knows about a subject, we can begin by exposing what we know.

Explain the subject first. Attempt the causal chain. Do the calculation. State what you think is happening and where you are uncertain. An attempted explanation makes the limits of understanding visible.

The model can then question it, identify missing links or misconceptions, change the level of explanation and test again.

There is also an important advantage over many human learning environments: very little social cost attaches to revealing ignorance. A senior analyst can ask an elementary question, admit that the explanation did not work, ask it again from another direction, or discover that something discussed for years was never properly understood.

There need be no embarrassment in finding the gap. Finding the gap is the point.

Used well, the model can create a repeated loop: attempt, expose, correct, test again.

The objective is not to make learning frictionless. It is to move the friction to the right place. Embarrassment, an explanation pitched at the wrong level, searching for the right material or waiting for somebody to be available are forms of friction we may happily reduce. Making the attempt, discovering the error, doing the calculation and demonstrating that we now understand are not.

## Better understanding, shared

This suggests two quite different roles for AI in an investment process.

The first is increasingly familiar. The model can do useful work: search, analyse, summarise, calculate, code or draft. As the intern test suggests, improving capabilities are making this more valuable.

The second is different. Rather than doing the work instead of us, the model can help us become better at doing the work ourselves.

Consider an analyst studying a semiconductor manufacturer. They might begin by explaining how they believe additional capacity will affect production, depreciation, margins and cash generation. Instead of simply returning its own explanation, the model can interrogate theirs. Which connections are sound? Which depend on unstated assumptions? Where has correlation been mistaken for causation? What calculation would test the argument? What question would best reveal whether the mechanism is actually understood?

A book or lecture has to choose a level in advance. A knowledgeable colleague can adapt, but their time is scarce. A model can repeatedly adjust its explanation, example or question in response to the learner's latest attempt.

None of this requires believing that a model can diagnose our knowledge perfectly. It cannot. Nor should we assume that increasing capability removes the possibility of error. These systems generate probabilistically, and while we can reduce errors by connecting them to authoritative sources, data and tools, we should not build an investment process that depends on errors disappearing.

The relevant risk is not simply how often a model is wrong. A single error can matter greatly if it sits in an analytically load-bearing part of an investment case and goes undetected.

For that reason, human responsibility remains essential. Domain expertise, pattern recognition, judgement and taste all matter in deciding whether an answer makes sense, what needs checking and which questions are worth asking in the first place. We expect the tools to become considerably more capable, but capability is not the same as responsibility. The analyst remains responsible for the work.

There is a longer-term point here too. Models are increasingly capable of executing complex tasks once an objective has been specified. We are less convinced that this removes the need for people to decide what is worth investigating, frame the problem, weigh competing perspectives and exercise judgement over long periods. Those are central parts of investing, rather than inconveniences around its edges.

And for FSSA, the intended beneficiary is not simply the individual analyst. It is the team's collective judgement.

A productive interaction with a model should therefore find its way back into the investment process. Sometimes that will be a clearer explanation in a research meeting, a better question for management or a reason to revisit something previously taken for granted. But the thing worth sharing may also be the method itself: a useful workflow, framework, tool, data connection or repeatable use case that helps colleagues do something better.

The opportunity is for individual learning to become organisational learning.

And here the governance example with which we began returns.

Apparent success is not sufficient evidence that a process is sound. More output is not necessarily better research. Agreement is not verification. A fluent explanation is not necessarily understanding.

The map we want is not simply more detailed. We want the economically important relationships represented more faithfully, assumptions made visible and areas of uncertainty marked as such.

There is a particular opportunity here for long-term investors. The outcome of an investment thesis may take years to become clear. We do not need to wait years to discover that we have misunderstood an accounting treatment, a manufacturing process or the source of a company's competitive advantage. Those are shorter learning cycles within a much longer investment process.

Better understanding does not guarantee a better investment result. Price still matters. Businesses change. Unexpected events occur. Sound analysis can still produce an unfavourable outcome.

But uncertainty about the eventual result is not a reason to be indifferent to the quality of the understanding that precedes it.

Our ambition is not to replace an established investment process with a succession of new tools. It is to bring better-informed people, more productive discussion and a clearer awareness of our own limitations to the process we already have.

Where there is interest, we are keen to share with clients in more detail some of the specific ways in which we are using AI to learn better. The tools will continue to change. Our objective is enduring: to keep improving the quality of understanding and judgement we bring to the long-term work of investing.

# Racing Your Own Ghost
## Part One: The ghost

The summer of 1993 was hot, or I remember it that way, and I spent most of it indoors with the curtains half drawn.

Super Mario Kart had arrived in Britain that January. There was a mode on it called Time Trial, with the shells and the banana skins and the other seven drivers all stripped out of it. Just you, one kart, an empty track, going round and round. On paper it is the dullest thing on the cartridge. It was the only thing I played.

Because it did have an opponent, after a fashion. The machine kept your best lap and set it running alongside you: a pale translucent copy of your own kart, taking every corner exactly the way you had taken it. You raced that. And when you beat it, the run that beat it quietly became the new thing to race.

Mushroom Cup, Mario Circuit One, for weeks — with one pause, on the fourth of June, for Shane Warne's ball of the century. And I chased hundredths of a second. Not seconds — hundredths. I learned that if you clipped one particular corner a hair tighter you came out of it fractionally quicker, and that the pale kart beside you would show you on the next lap exactly where you had found the time and exactly where you had given it back.

If I were ever stopped at the Pearly Gates and asked where, specifically, I had tried hardest in life, sharpened my powers most keenly, the honest answer is that game, that one course, across the eternal-seeming summer of 1993, against a ghost of myself.

I did not think about it again for thirty years.

## Part Two: The actor and the critic

Then a couple of years ago I came across the most astonishing thing I have ever read, and it sent me straight back to that bedroom.

It is in Max Bennett's A Brief History of Intelligence, a marvellous book whose frequent method is to catch the same trick appearing twice — once in a nervous system and once in a machine. It goes like this. Through the late 1980s and early 1990s the neurophysiologist Wolfram Schultz put electrodes into the midbrain of monkeys, recording from the cells that release dopamine, the chemical everyone had long since filed under pleasure. He gave the monkeys a drop of juice and watched the cells fire. Reward in, then a clean burst of dopamine, exactly as everyone expected. Fine. Then he looked more carefully, and the pleasure story fell apart.

Two more things, and these are the interesting ones. When a light reliably preceded the juice, so the animal learned to expect it, the burst walked backwards in time: it left the juice and attached itself to the light, to the earliest thing that predicted the reward, and the juice itself, now fully expected, drew no response at all. And when the light came but the promised juice did not, at the exact moment the juice was due, the firing dipped below its resting rate. It went quiet in disappointment, on schedule.

What the cell reports is any gap between what was predicted and what arrived — surprise upward, disappointment downward, silence when the world unfolds exactly as guessed. It is an error signal, and it had been sitting in plain sight for years being called a pleasure signal.

Years earlier Richard Sutton, one of the founders of reinforcement learning, had been working on a problem that had nothing to do with brains. Suppose you want to build something that learns to play a game. It makes a hundred moves and then the world says won or lost. One number, at the end, for the whole performance. Somewhere in there, move thirty was the one that quietly but irreversibly tipped the scales in your favour. How is the machine supposed to find that out?

Crediting move ninety-nine gets you nowhere; it was a formality. Spreading the credit evenly across all hundred is worse because the positive signal from move thirty is smeared away to nothing. You could hire somebody to mark each move as it happens, except that a teacher who already knows which moves were good is precisely what you do not have.

Sutton's answer was to stop waiting for the result. You already carry an estimate of how well things are going. Make a move. Look at where it lands you, and read off the estimate for that. If the second number is better than the first, the first was too low — so raise it, and credit the move that made the difference. No teacher is consulted, and nothing has to finish. The signal is the change in expectation from one moment to the next. It has a name: the temporal difference.

Which implies a division of labour. One thing has to play, sitting inside the game and choosing, move by move. Another has to hold the running estimate and revise it. Call them the actor and the critic. The actor moves; the critic, a moment later, says whether things now look better or worse than it had been expecting; the actor adjusts accordingly. Neither is any good at the start, and each is working entirely from the other's output. Yet across enough games the two of them ratchet upward, every gain in one making the other's job a little more possible. That is the part that looks like sleight of hand, and it took me a long time to be satisfied about it.

Peter Dayan, Read Montague and Terrence Sejnowski knew Sutton's work, and they recognised it in Schultz's recordings. The dopamine neuron was computing Sutton's term. It had been computing it, in one vertebrate midbrain or another, for hundreds of millions of years before anybody wrote it down.

And it is there in yours right now, delivering that slight pall of disappointment caused by the fact that you don't agree — hopefully yet — that this is the most astonishing thing you have ever read. That flatness is the dip I described a moment ago: a predicted reward that has not arrived. Reading that line, just now, you were the disappointed monkey.

Bennett's move is to site that machinery in the brain. The actor is the basal ganglia — present and recognisable in the lamprey, which parted company from us something like 560 million years ago, and older by far than any monkey. It spends its life inhibiting, holding down every possible action at once, and choosing by releasing its grip on one of them. The critic is the dopamine system, scoring each of the actor's choices against its own shifting prediction of the reward. No one outside is grading the moves. The brain generates the standard itself, and pushes it up every time the actor improves, so getting better never makes the grading any kinder.

## Part Three: The thing Bennett walks past

Bennett calls this a magical bootstrapping. And then he moves on, as he must, with several hundred million years of brain evolution still ahead of him. I got stuck.

Magic is only a trick you have not been shown yet, and I wanted to see it. So I went and looked — David Silver's lecture course, the textbook, the papers people cite when they are being careful.

What needs explaining is a circle. The critic can only learn what a position is worth by watching the actor play, so its numbers are an accurate account of a poor player. The actor can only tell a good move from a bad one by asking the critic. Each is the other's only source of information, and both start with nothing to go on. Left alone, an arrangement like that should simply cement its first mistakes: a set of numbers that agree with each other perfectly and mean nothing.

Three things stop the cement from drying.

The first is that something real happens at the end. Every estimate is checked against the next estimate along, which sounds sealed shut — until the game ends. Then there is no next estimate, only an outcome, and the outcome arrives from outside and does not care what was predicted. That last correction is real. Next time through, the second-to-last estimate is checked against the now-corrected last one, and truth walks backwards a link at a time until it reaches the opening move. Everybody in a bucket chain is only ever handed something by the person beside them — a closed loop, until you notice that the one at the far end is standing in the river.

The second is that the actor and the critic are allowed to move at different speeds. The critic's numbers describe the actor as it currently is, so improving the actor makes every number stale. Let the critic revise quickly and the actor drift slowly, and each can treat the other as furniture. It is the productive fudge a chemist makes when she solves for the fast electrons with the slow nucleus held fixed. The nucleus is moving. It is just so slow, beside an electron, that pretending otherwise costs nothing.

The third is that the actor asks less of the critic than you would think. It does not need the numbers to be accurate. It needs the better of two options ranked above the worse one, and nothing else. A critic can be wrong about everything by some wandering amount and still be enough: switch to the higher-ranked option everywhere and you come out at least as good as you were, and better unless you were already perfect.
So the trick has been shown. An anchored chain, a difference in speeds, and a ratchet under the one that acts — and none of it needs a teacher, or either party to be any good at the start.

Two things happened when I understood it.

The magic did not go anywhere. I had expected the mathematics to dissolve it and instead it sharpened it, which I think is the ordinary experience of being shown how a trick is done well.

And the explanation turned out to be incomplete. Every part of it describes what happens once the attempts are coming in. Not one word of it says where the attempts come from, or who you are supposed to be practising against. The loop assumes a supply of games worth playing, and the world does not reliably provide one.

## Part Four: The right band

So where does the practice come from? And what kind of practice works best?

An opponent has to meet a fairly narrow specification to teach you anything. Somebody who beats you soundly every time hands you the same result whatever you do, so nothing in it can pick out the moves that were slightly less bad than the rest. Somebody who never beats you leaves you free to keep every bad habit you have, because none of them ever costs anything. What you want is a Goldilocks opponent, one who takes about half. Close enough that the difference between your better and worse decisions shows up in the result, and far enough ahead to stretch you without breaking you.

Mihaly Csikszentmihalyi spent a career on that band and gave it a name. Flow arrives when what a task demands and what you can do are close to level. Push the demand too far above the skill and you get anxiety; let it fall below and you get boredom; and in the narrow space between them people report losing an afternoon without noticing.

I lost a summer.

He set two more conditions beside it — a goal you cannot mistake, and feedback quick enough to act on. The part that matters here is that the channel will not hold still. Get better and yesterday's challenge slides down into boredom, so staying inside it means the difficulty has to climb at roughly the rate you do.

Which almost nothing can manage. But a recording of your own last run does it, for nothing.

It is the best you have ever been, which is another way of saying it is very slightly worse than you are about to be. You beat it by a hundredth, the new run takes its place, and now you are chasing something a hundredth quicker than the thing you just beat. Nobody sets the level. It rises because the evidence rose — you have just proved that the faster lap belongs inside the set of things you can do, so that is where the edge sits now. No other standard is guaranteed to sit exactly where you can nearly reach it.

And it tells you something a scoreline cannot. A time at the end of a lap says the lap was slower. The pale kart says where: level with you at the first corner, a length up at the third, and the gap between those two facts is the corner you got wrong. A verdict on one decision, arriving while you are still driving.

So a thirteen-year-old with a cartridge had all three of Csikszentmihalyi's conditions in front of him at once, supplied by a machine that was not trying to supply them and did not know he was there.

That is self-play, more or less. Set a machine to play itself and the problem dissolves by construction: whatever it can currently do is exactly the thing it has to beat. AlphaGo Zero began knowing the rules of Go and nothing else, played itself, and inside three days had passed the version that beat Lee Sedol, having never been shown a single game between human beings.

The ladder it climbed was built out of its own earlier attempts, every rung set one step above the last, by nobody.

## Part Five: Two powers

Everything so far has been one engine: an actor, a critic, and a standard that climbs as the actor does. It has been turning in vertebrate brains for half a billion years, which is why it shows up in a lamprey. What changed is that a second engine arrived for the first to be coupled to.

The second engine is gradient descent. It grew up in a separate tradition, running alongside reinforcement learning for decades without much needing it, and it is surprisingly simple to describe. Imagine being set down blindfolded on a hillside and told to get to the bottom. You reach out a foot; you feel whether the ground there is lower; if it is, you step to it. Then repeat. That is the entire algorithm. It requires you to understand nothing about the hill, and it will reliably walk you to the bottom of whatever valley you happen to have landed in.

Now put that at the heart of a neural network. Start with a pile of data and a model that is nothing but random numbers in a mess. Define the loss — the gap between what the model produced and what was wanted — and treat that as your height on the hill. Nudge every weight slightly in whatever direction lowers it, and repeat. Gradient descent takes the step; backpropagation works out which way is down, sensing the whole slope at once instead of one foot at a time. The pairing is the only reason any of this works in a space of a billion dimensions. That is modern pretraining. Everything that has come out of a chat window came out of that loop.

Deep reinforcement learning — actor and critic computing their answers with a neural network instead of looking them up in a table — is the two engines married. Descent will fit a network to whatever target it is given, and a fitted network can judge positions nobody ever showed it. The bootstrap is what supplies the target — one nobody wrote down, which rises as the actor improves. AlphaGo Zero arranges the same two parts differently: improvement found by searching ahead, then stored in the network by descent, so that the next search sets out from a stronger network.

Neither engine alone gets you here. Both together, with enough silicon to run on and enough electricity to burn, have changed our place in the world, perhaps forever. The Himalayas are only what happens when two things that were travelling separately collide, and the sole remaining direction is up. Burke's name for what a person feels looking at them was the sublime, and he meant it more strictly than we do: astonishment with a degree of horror in it, available only from a safe distance. The ranges going up around us now are new, and still rising, and I am not sure where the safe distance is.

## Part Six: It was always games

That leaves us to attend to the serious business of fun.

From here the essay stops being a line and turns into a braid. The same few names keep appearing in one another's stories, and the same ideas keep being discovered by people who did not know they had been discovered already. I have given up trying to straighten it out.

In 1969 a programmer at Bell Labs named Ken Thompson wrote a game called Space Travel — a little simulation of the solar system, in which you flew a ship about and tried to set it down on the various moons. The trouble was that every go cost something like seventy-five dollars of the lab's money. So he found a computer nobody was using, a P D P 7 in a corner with a good display hanging off it, and set about moving his game onto it, which turned out to mean writing from scratch a floating-point package, the shapes of the characters on the screen, and a debugger — all of it prepared on another machine and walked over on paper tape. Thompson's need to play the game took him to that corner of the room and made him fluent in the machine sitting in it, and it was there, a few months later, that he wrote the first version of Unix. Most of the internet now runs on its descendants.

His people wrote the reason down. Eric Raymond's The Art of Unix Programming has a section headed "Unix Is Fun to Hack". Raymond defines the fun: it arrives "when the effort they have to put out to do a task challenges them, but is just within their capabilities."

Which is the flow channel, derived independently, by a man writing about operating systems.

Once you are looking for it, it is everywhere. The shell most of Thompson's descendants run on is called Bourne Again. One program for reading a file was named more. The one that came after it, which could also scroll backwards, was named less.

Raymond also quotes Thompson on what to do when you are stuck. When in doubt, use brute force. Sixteen years later Sutton published an essay arguing that the methods which win in the long run are the ones that simply use more computation, and that the field keeps refusing to believe it. He called it the bitter lesson. Thompson had it as a joke.

Thirty years on from the P D P 7, two friends from Cambridge were making video games for a living: Demis Hassabis, who had been designing them since he was a teenager, and David Silver, who was his lead programmer. Silver left for Alberta to take a doctorate under Richard Sutton, on temporal difference learning turned loose on the game of Go. He finished it in 2009. On the acknowledgements page he wrote: "Rich Sutton has been a constant source of inspiration and wisdom… I'd also like to thank Gerry Tesauro for his keen insights and many constructive suggestions."

Some years later the two friends were back in the same building, in a company whose whole method was to build things that got good at games. Watching them do it, and being frightened by it, is why much of the rest of the industry exists at all.

Which is neither coincidence nor quite a joke. The ratchet has two requirements in order to run. It needs repetition, because it climbs in tiny increments, each one measured against its own last attempt. And it needs an honest verdict from somewhere outside itself, one number it did not produce, or the chain of guesses starts vouching for its own mistakes. Very little in ordinary life supplies both, but a game does. A small world you can enter again, and again, and again, and a score at the end of it that cannot be sweet-talked.

That is half of it. The other half is why anyone was in the room to begin with. Remember what the dopamine burst did when the light came on? It moved. It left the juice and attached itself to the promise.

Which is a peculiar fact about you too: you are not paid by your dopamine system when you win. You are paid at the moment you feel winning becoming likely. Most of the world knows the flatness that arrives after a victory, a destination reached.

And the cells doing the paying are the cells doing the teaching. Anticipation and instruction are one mechanism, felt from the inside and measured from the outside.

The reason a game teaches you and the reason you cannot put it down are the same — which is how a boy could give a whole summer to one lap of one track, get steadily better at it, and never once experience it as work.

For three decades the joke among the unimpressed was that reinforcement learning was a technique for winning at things that did not matter. Chess, backgammon, Atari, Go, so what?

But then the world noticed that the referee was the point, and the game was only ever the easiest place in the world to find one — something outside the learner that can look at an attempt and hand back a verdict that will not negotiate. Put it that way and the question becomes: what else has a referee?

Code does. Run the tests. They pass or they don't, and confidence in the code does not move the result by a millimetre.

Mathematics does. A proof checker reads a formal argument and accepts it or refuses it, with no interest in who wrote the argument or how certain they felt while writing it.

And the people inside that field have been telling us for a century. Mathematicians talk about their work in the vocabulary of play as a matter of course — elegance, beautiful moves, a problem you cannot put down — and they name their results accordingly: the hairy ball theorem, the ham sandwich theorem, the happy ending problem. Hardy, in the book he wrote to justify a life spent on pure mathematics, paused to observe that chess problems are the hymn-tunes of mathematics. Erdős is the funniest case rather than the only one: he called God the Supreme Fascist, called children epsilons, kept an imaginary volume of the perfect proofs that he referred to as The Book, and paid cash out of his own pocket for problems he could not do himself.

Programming and mathematics look like the two most solemn things a person can do, yet they are the two places where you find out immediately, and without appeal, whether the thing you just tried worked. Which is what a game is. Reinforcement learning did not escape the games. It found out how many things had been games all along.

There is a name for training this way now — reinforcement learning from verifiable rewards — and a law to go with it. Jason Wei, a researcher at OpenAI, named it the Verifier's Law in 2025: how easily a machine can be taught a task is proportional to how easily the task can be checked. Anything doable and cheaply checked will get done.

At the start of 2025 the Chinese laboratory DeepSeek published an intermediate model called R1 Zero, trained by that method and nothing else: no worked examples of human reasoning, no demonstrations to copy, only problems with checkable answers and a signal that said yes or no. Long chains of reasoning appeared in it that nobody had put there. The paper records an intermediate version writing "Wait, wait. Wait. That's an aha moment I can flag here," and the authors note, mildly, that they had not taught it to do that. They set the incentive and let it find the behaviour. Which is the ghost again, and the ratchet, and a critic scoring an actor. On some systems the reinforcement stage now burns more computation than the reading of the entire internet that came before it.

By the hot, hot summer of 2026 that marriage was cracking problems in mathematics that had resisted the finest human minds for decades. In May a model produced a counterexample to a conjecture of Erdős about unit distances, open since 1946; nine mathematicians co-signed the verification, and Timothy Gowers, a Fields medallist at Cambridge, said he would recommend it without hesitation to the Annals of Mathematics, which publishes perhaps thirty papers a year and is the most selective journal in the subject. At the start of August, less than a week ago as I write, OpenAI used an unreleased model called Astra to publish ten results in mathematics and theoretical computer science, each one shipped with a machine-checkable certificate, on problems where nothing had moved for at least a decade. Within a day somebody had reproduced five of them on a Claude model anyone can buy. Terence Tao now puts these systems on a par with a junior co-author. Gowers and Tao both hold the Fields Medal, and neither is a man given to enthusiasm.

## Part Seven: Summer 1993

That summer, none of the rest of it had happened. At IBM Gerald Tesauro was watching TD-Gammon climb to a level he had not believed a machine could reach, and would take it to Bill Robertie, twice a world champion, and lose by one point across forty games. Schultz's monkeys had given up the second of the three findings that spring — the paper showing the burst walking backwards onto the light — and the dip below the resting rate took another five years to arrive. AlphaGo was twenty-three summers off. A few weeks earlier, in a Denny's in San Jose, Jensen Huang and two friends had founded a company to build better graphics chips for video games. The whole internet had about fourteen million people on it, and had begun that year with fewer than a hundred websites.

And in a bedroom with the curtains still half drawn, a record bought that June was playing for the hundredth time, and the sparkling electric piano at the top of "Blow Your Mind" came out of a small speaker while he lined up one more lap.

He had no idea. He was just going round again.

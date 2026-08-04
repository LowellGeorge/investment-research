# The Ghost Car
## Part One: The ghost

The summer of 1993 was hot, or I remember it that way, and I spent most of it indoors with the curtains half drawn.

Super Mario Kart had arrived in Britain that January. There was a mode on it called Time Trial, with the shells and the banana skins and the other eleven drivers all stripped out of it. Just you, one kart, an empty track, going round and round. On paper it is the dullest thing on the cartridge. It was the only thing I played.

Because it did have an opponent, after a fashion. The machine kept your best lap and set it running alongside you: a pale translucent copy of your own kart, taking every corner exactly the way you had taken it. You raced that. And when you beat it, the run that beat it quietly became the new thing to race.

Mushroom Cup, Mario Circuit One, for weeks — with one pause, on the fourth of June, for Shane Warne's ball of the century. And I chased hundredths of a second. Not seconds — hundredths. I learned that if you clipped one particular corner a hair tighter you came out of it fractionally quicker, and that the pale kart beside you would show you on the next lap exactly where you had found the time and exactly where you had given it back.

If I were ever stopped at the Pearly Gates and asked where, specifically, I had tried hardest in life, the honest answer is Super Mario Kart, Time Trial, Mario Circuit One, the first course of the Mushroom Cup, summer of 1993, against a ghost of myself. Not my education. Not any of the work I have been paid for. It is also the closest I have come to the ceiling of a thing.

I did not think about it again for thirty years.

## Part Two: Thirty years later

Then a couple of years ago I came across the most astonishing thing I have ever read, and it sent me straight back to that bedroom.

It is in Max Bennett's A Brief History of Intelligence, a book whose method is to catch the same trick appearing twice — once in a nervous system and once in a machine. It goes like this. Through the late 1980s and early 1990s the neurophysiologist Wolfram Schultz put electrodes into the midbrain of monkeys, recording from the cells that release dopamine, the chemical everyone had long since filed under pleasure. He gave the monkeys a drop of juice and watched the cells fire. First: reward, dopamine as expected. Fine. Then he looked more carefully, and the pleasure story fell apart.

Three things. When the juice arrived unannounced, the neuron fired — a clean burst. When a light reliably preceded the juice, so the animal learned to expect it, the burst walked backwards in time: it left the juice and attached itself to the light, to the earliest thing that predicted the reward, and the juice itself, now fully expected, drew no response at all. And when the light came but the promised juice did not, at the exact moment the juice was due, the firing dipped below its resting rate. It went quiet in disappointment, on schedule.

Those last two are the interesting ones. A fully predicted reward earns silence. What the cell reports is the gap between what was predicted and what arrived — surprise upward, disappointment downward, silence when the world unfolds exactly as guessed. It is an error signal, and it had been sitting in plain sight for years being called a pleasure signal.

Years earlier Richard Sutton, one of the founders of reinforcement learning, had come at the same thing from the other end, and the problem he was working on is easy to state. Suppose you want to build something that learns to play a game. It makes a hundred moves and then the world says won or lost. One number, at the end, for the whole performance. Somewhere in there, move thirty was the one that did it — the quiet developing move that made everything afterwards possible. How is the machine supposed to find that out?

Crediting move ninety-nine gets you nowhere; it was a formality. Spreading the credit evenly across all hundred is worse because the positive signal from move thirty is smeared away to nothing. You could hire somebody to mark each move as it happens, except that a teacher who already knows which moves were good is precisely what you do not have.

Sutton's answer was to stop waiting for the result. Judge each position against your own estimate of the position that comes after it. If things look better a moment later than you had expected them to look, that is good news, and the move that got you there can be credited immediately — not at the end of the game, and not by anybody. The signal is the change in expectation from one moment to the next. It has a name: the temporal difference.

Which implies a division of labour. One thing has to play, sitting inside the game and choosing, move by move. Another has to hold the running estimate and revise it. Call them the actor and the critic. The actor moves; the critic, a moment later, says whether things now look better or worse than it had been expecting; the actor adjusts accordingly. Neither is any good at the start, and each is working entirely from the other's output. Yet across enough games the two of them ratchet upward, every gain in one making the other's job a little more possible. That is the part that looks like sleight of hand, and it took me a long time to be satisfied about it.

Peter Dayan, Read Montague and Terrence Sejnowski knew that mathematics, and they recognised it in Schultz's recordings. The dopamine neuron was computing Sutton's term. The equation was already running, in a monkey's midbrain, hundreds of millions of years before anyone wrote it down.

And it is there in yours right now, delivering that slight pall of disappointment caused by the fact that you don't agree — hopefully yet — that this is the most astonishing thing you have ever read. That flatness is the dip I described a moment ago: a predicted reward that has not arrived. Reading that line, just now, you were the disappointed monkey.

Bennett's move is to site that machinery in the brain. The actor is the basal ganglia — present and recognisable in the lamprey, which parted company from us something like 560 million years ago, and older by far than any monkey. It spends its life inhibiting, holding down every possible action at once, and choosing by releasing its grip on one of them. The critic is the dopamine system, scoring each of the actor's choices against its own shifting prediction of the reward. No one outside is grading the moves. The brain generates the standard itself, and pushes it up every time the actor improves, so getting better never makes the grading any kinder.

## Part Three: The thing Bennett walks past

Bennett calls this a magical bootstrapping. And then he moves on, as he must, with several hundred million years of brain evolution still ahead of him. I got stuck.

A position is only as good as the actor's ability to exploit it, so the critic's judgement is hostage to the actor's skill; and the actor can learn only from a critic whose judgements are sound, so its skill is hostage to the critic. Each one's competence depends on the other's.

Nobody supplies the value of every position. There is no answer key, and no adult in the room saying this much and no more. The world contributes an occasional verdict — the juice, the win, the lap time — and leaves actor and critic to manufacture almost everything in between. Somehow the pair climb instead of merely confirming one another's first mistakes.

That it works is settled. It worked in simulation, and then in 1992 inside TD-Gammon, Gerry Tesauro's backgammon program at IBM, which taught itself by Sutton's method until it reached master level, came within a single point of a world champion over forty games, and rewrote the opening theory of a game people had studied for centuries. Twenty-four years later AlphaGo's thirty-seventh move against Lee Sedol made the same point to a rather larger audience. We will come back to this territory, because the same method, married to deep learning and run at enormous scale, is most of the reason the last two years have gone the way they have.

Which tells us the loop can be trusted, and tells us nothing about why. Something must stop a bootstrapped error becoming the teacher of the next one, and calling the result convergence only gives that something a name.

Magic is a fair word for it. But magic is only a trick you have not been shown yet. So: how does it actually work?

## Part Four: Inside the loop

Two jobs, and neither can be done properly until the other one has been.

The actor can only tell a good move from a bad one by asking the critic. The critic can only learn what a position is worth by watching the actor play, so its numbers are an accurate account of a poor player. Each is the other's only source of information. Both start with nothing to go on.

Three things save it.

The chain has an end, and the end is real.

The critic's verdict on where things stand is checked against its verdict on where things stand a moment later. Which sounds sealed shut — every number vouched for by another number from the same source. But run the thing forward far enough and there is no next moment. There is an outcome: won, lost, juice, no juice. It arrives from outside and it does not care what was predicted. So the last verdict in the chain gets corrected against something real. Next time through, the second-to-last is checked against that now-corrected last one, and becomes a little truer itself. The time after, the third-to-last. Truth enters at a single point and walks backwards, one link per pass, until it has reached the opening move.

Everybody in a bucket chain is only ever handed something by the person beside them — a closed loop, until you notice that the one at the far end is standing in the river.

There is no fixed teacher, and there is a fixed point. Nobody holds the right answer. And yet a right answer exists — one set of numbers that square with each other and with the outcome — and the apparatus is feeling towards it in the dark.

One of them moves slowly.

The critic's numbers describe the actor as it currently is. Improve the actor and every number goes stale: an accurate account of somebody who no longer exists. So the critic never arrives. Each time it closes in, the target gets up and walks off. Two things in motion, each quietly redefining the problem the other is working on.

They meet because the speeds differ. The critic revises constantly; the actor drifts. Across the many revisions it takes the actor to become meaningfully different, the critic has caught up over and over. So each is entitled to treat the other as furniture — the critic because the actor is nearly standing still, the actor because the critic is nearly right about the player it currently is.

It is the productive fudge a chemist makes when she solves for the fast electrons with the slow nucleus held fixed. The nucleus is moving. It is just so slow, beside an electron, that pretending otherwise costs nothing.

Konda and Tsitsiklis proved it around the turn of the century, though only for a restricted family of these algorithms.

The actor only needs the ranking to be right.

Grant both of those and the pair holds together. A thing can hold together and go nowhere.

The demand the actor makes on the critic is smaller than it looks. It needs the better of two options placed above the worse one, and it needs nothing else. Every number can be too high, or too low, or wrong by some wandering amount, and it will not matter — so long as the order is right, an actor that switches to the higher-ranked option everywhere comes out at least as good as it was, and strictly better unless it was already perfect.

That is a theorem, and it is what keeps the arrangement honest. A badly calibrated critic is still a useful one, provided it knows which of two things is better. Improvement then ratchets: judge how it plays, act on the judgement, arrive at a better player, judge that. Each turn of the crank is guaranteed not to go backwards, and the gain never has to be handed back.

*

Those three keep the loop upright. What makes it get rich — why something that starts with one bit a game ends up knowing a hundred thousand things — is the dependence that looked like the problem to begin with. A slightly better critic lets the actor tell apart two moves it had been treating as identical. Acting on that difference takes it somewhere neither of them has been, which the critic has never had to assess. Assessing it sharpens the critic, whose new distinctions change the actor again. Neither of them is working to a plan. Each keeps handing the other something it has not seen before.

So the mutual dependence Bennett calls magical is doing the work. Two learners, tied at one end to something that actually happened, moving at speeds far enough apart to hold still for one another, with a ratchet under the one that acts. None of it needs a teacher. None of it needs either of them to be any good to start with.

One thing is missing, and it is exactly what kept me improving relentlessly at a simple racing game in the summer of 1993.

## Part Five: The right band

So where does the practice come from? And what kind of practice works best?

The actor learns from what it does; the critic learns from watching. Neither of them picks the opposition. The arrangement assumes a supply of games worth playing, and the world does not reliably provide one.

An opponent has to meet a fairly narrow specification to teach you anything. Somebody who beats you soundly every time hands you the same result whatever you do, so nothing in it can pick out the moves that were slightly less bad than the rest. Somebody who never beats you leaves you free to keep every bad habit you have, because none of them ever costs anything. What you want is a Goldilocks opponent, one who takes about half. Close enough that the difference between your better and worse decisions shows up in the result, and far enough ahead to stretch you without breaking you.

Mihaly Csikszentmihalyi spent a career on that band and gave it a name. Flow arrives when what a task demands and what you can do are close to level. Push the demand too far above the skill and you get anxiety; let it fall below and you get boredom; and in the narrow space between them people report losing an afternoon without noticing.

I lost a summer.

He set two more conditions beside it — a goal you cannot mistake, and feedback quick enough to act on. The part that matters here is that the channel will not hold still. Get better and yesterday's challenge slides down into boredom, so staying inside it means the difficulty has to climb at roughly the rate you do.

Which almost nothing can manage. Most of the apparatus around competitive practice exists to fake it: leagues and divisions, handicaps in golf, a coach who knows the week to stop going easy on you. All of it is machinery for producing an opponent one notch above the player, and all of it costs clubs and institutions and other people's afternoons.

A recording of your own last run is the same thing, for nothing.

It is the best you have ever been, which is another way of saying it is very slightly worse than you are about to be. You beat it by a hundredth, the new run takes its place, and now you are chasing something a hundredth quicker than the thing you just beat. Nobody sets the level. The level is whatever you last managed — the one measure certain to sit exactly where you can nearly reach it, and certain to move up the moment you do.

And it tells you something a scoreline cannot. A time at the end of a lap says the lap was slower. The pale kart says where: level with you at the first corner, a length up at the third, and the gap between those two facts is the corner you got wrong. A verdict on one decision, arriving while you are still driving.

So a thirteen-year-old with a cartridge had all three of Csikszentmihalyi's conditions in front of him at once, supplied by a machine that was not trying to supply them and did not know he was there.

That is self-play, more or less. Set a machine to play itself and the problem dissolves by construction: whatever it can currently do is exactly the thing it has to beat. AlphaGo Zero began knowing the rules of Go and nothing else, played itself, and inside three days had passed the version that beat Lee Sedol, having never been shown a single game between human beings.

The ladder it climbed was built out of its own earlier attempts, every rung set one step above the last, by nobody.

## Part Six: Two powers

Everything so far has been one engine: an actor, a critic, and a standard that climbs as the actor does. It has been turning in vertebrate brains for half a billion years, which is why it shows up in a lamprey. What changed is that a second engine arrived for it to be coupled to.

The second engine is gradient descent. It grew up in a separate tradition, running alongside reinforcement learning for decades without much needing it, and it takes a paragraph to describe. Imagine being set down blindfolded on a hillside and told to get to the bottom. You reach out a foot; you feel whether the ground there is lower; if it is, you step to it. Then again. That is the entire algorithm. It requires you to understand nothing about the hill, and it will reliably walk you to the bottom of whatever valley you happen to have landed in.

Now put that at the heart of a neural network. Start with a pile of data and a model that is nothing but random numbers in a mess. Define the loss — the gap between what the model produced and what was wanted — and treat that as your height on the hill. Nudge every weight slightly in whatever direction lowers it, and repeat. Gradient descent takes the step; backpropagation works out which way is down, computing the slope in every direction at once rather than feeling for it one foot at a time. The pairing is the only reason any of this is feasible in a space of a billion dimensions. That is modern pretraining, in its entirety. Everything that has ever come out of a chat window came out of that loop.

There is no bootstrap anywhere in it. Nothing hauls on its own laces. The hill does not move, and something walks patiently downhill toward a bottom that was fixed before it set out; the walk can be very hard to do well, and large training runs come off the rails often enough, but it cannot talk itself into a mistake. Nothing under the ratchet holds still. It has to manufacture its own target and then keep raising it, which is why it needs a thin line of outside truth and a difference in speeds even to hold together.

Deep reinforcement learning — actor and critic computing their answers with a neural network instead of looking them up in a table — is the two engines married. Descent supplies machinery that can judge a position it has never seen before; the bootstrap supplies the ever-rising target for it to walk toward. AlphaGo Zero arranges the same two parts differently. Its improvement comes from search. Out of the position in front of it the machine grows a tree — this move, then the reply, then the reply to that — millions of continuations, steered at every branch by the network's own hunches about which are worth following. It arrives somewhere better than it could have reached in a single glance. Then the tree is thrown away. Nothing is kept unless the network is trained toward what the search found, which is plain descent, target fixed, walking downhill. Improvement discovered by search and stored by descent — and the better network makes the next search stronger still.

Neither engine alone gets you here. Both together, with enough silicon to run on and enough electricity to burn, are what the last ten years have been. The Himalayas are only what happens when two things that were travelling separately collide, and the sole remaining direction is up. Burke's name for what a person feels looking at them was the sublime, and he meant it more strictly than we do: astonishment with a degree of horror in it, available only from a safe distance. The ranges going up around us now are new, and still rising, and I am not sure where the safe distance is.

## Part Seven: It was always games

That leaves the serious business of fun.

By 1969 a programmer at Bell Labs named Ken Thompson had written a game called Space Travel — a little simulation of the solar system, in which you flew a ship about and tried to set it down on the various moons. The trouble was that every go cost something like seventy-five dollars of the lab's money. So he found a computer nobody was using, a P D P 7 in a corner with a good display hanging off it, and set about moving his game onto it, which turned out to mean writing from scratch a floating-point package, the shapes of the characters on the screen, and a debugger — all of it prepared on another machine and walked over on paper tape. Thompson's need to play the game took him to that corner of the room and made him fluent in the machine sitting in it, and it was there, a few months later, that he wrote the first version of Unix. Most of the internet now runs on its descendants.

His people wrote the reason down. Eric Raymond's The Art of Unix Programming has a section headed "Unix Is Fun to Hack", and it is faintly embarrassed about it — programmers, Raymond says, "seem almost ashamed to acknowledge this sometimes, as though admitting they're having fun might damage their legitimacy somehow." Then he defines the fun. It arrives "when the effort they have to put out to do a task challenges them, but is just within their capabilities."

Which is the flow channel, derived independently, by a man writing about operating systems.

Once you are looking for it, it is everywhere. The shell most of Thompson's descendants run on is called Bourne Again. One program for reading a file was named more. The one that came after it, which could also scroll backwards, was named less. Erdős — whose conjecture about unit distances a machine would break in May — called God the Supreme Fascist, called children epsilons, kept an imaginary volume of the perfect proofs that he referred to as The Book, and paid cash out of his own pocket for problems he could not do himself. The results in that field have names like the hairy ball theorem, the ham sandwich theorem, and the happy ending problem.

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

There is a name for training this way now — reinforcement learning from verifiable rewards — and a law to go with it. Jason Wei, a researcher at OpenAI, stated it in 2025: how easily a machine can be taught a task is proportional to how easily the task can be checked. Anything doable and cheaply checked will get done.

At the start of 2025 the Chinese laboratory DeepSeek published a model trained by that method and nothing else: no worked examples of human reasoning, no demonstrations to copy, only problems with checkable answers and a signal that said yes or no. Long chains of reasoning appeared in it that nobody had put there. The paper records an intermediate version writing "Wait, wait. Wait. That's an aha moment I can flag here," and the authors note, mildly, that they had not taught it to do that. They set the incentive and let it find the behaviour. Which is the ghost again, and the ratchet, and a critic scoring an actor. On some systems the reinforcement stage now burns more computation than the reading of the entire internet that came before it.

By the hot, hot summer of 2026 it had reached mathematics that human beings had stopped being able to move. In May a model produced a counterexample to a conjecture of Erdős about unit distances, open since 1946; nine mathematicians co-signed the verification, and Timothy Gowers, a Fields medallist at Cambridge, said he would recommend it without hesitation to the Annals of Mathematics, which publishes perhaps thirty papers a year and is the most selective journal in the subject. At the start of August, less than a week ago as I write, OpenAI used an unreleased model called Astra to publish ten results in mathematics and theoretical computer science, each one shipped with a machine-checkable certificate, on problems where nothing had moved for at least a decade. Within a day somebody had reproduced five of them on a Claude model anyone can buy. Terence Tao now puts these systems on a par with a junior co-author. Gowers and Tao both hold the Fields Medal, and neither is a man given to enthusiasm.

Bennett's claim was about lampreys and monkeys: that this loop is what intelligence looks like whenever it has to get better with nobody to teach it. The same loop is now packing spheres in high dimensions.

Programming and mathematics look like the two most solemn things a person can do, yet they are the two places where you find out immediately, and without appeal, whether the thing you just tried worked. Which is what a game is.

That summer, none of the rest of it had happened. At IBM Gerald Tesauro was watching TD-Gammon climb to a level he had not believed a machine could reach, and would take it to Bill Robertie, twice a world champion, and lose by one point across forty games. Schultz's monkeys had given up the second of the three findings that spring — the paper showing the burst walking backwards onto the light — and the dip below the resting rate took another five years to arrive. AlphaGo was twenty-three summers off. A few weeks earlier, in a Denny's in San Jose, Jensen Huang and two friends had founded a company to build better graphics chips for video games, which, given everything above, may be the least surprising sentence in this essay. The whole internet had about fourteen million people on it, and had begun that year with fewer than a hundred websites.

And in a bedroom with the curtains still half drawn, a record bought that June was playing for the hundredth time, and the sparkling electric piano at the top of "Blow Your Mind" came out of a small speaker while he lined up one more lap.

He had no idea. He was just going round again.

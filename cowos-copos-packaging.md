# Chips on Wafers, Chips on Panels: How AI Packaging Actually Works

An audio walk through advanced semiconductor packaging — from the technology that bottlenecks the entire AI boom, to the shift that could unlock it.

---

Let me start with the single most important idea, because everything else hangs off it.

For decades, the hard part of making a chip was the chip itself — shrinking transistors, cramming more of them onto a piece of silicon. That is still hard. But something quietly inverted around the time the AI boom took off. The binding constraint on how much AI compute the world can build is no longer the logic die. It is the packaging — the business of wiring that die to its memory and mounting the whole thing so it can run.

Here is the number that makes it concrete. Take a Blackwell B200, Nvidia's flagship AI processor. The two graphics-processor dies inside it — the actual compute silicon — cost about nine hundred dollars to make. The packaging that connects those dies to their memory costs about eleven hundred dollars. The packaging costs more than the chips. That is a historic reversal, and it means the company that controls the best packaging controls the pace of the AI build-out. That company is T-S-M-C, and the technology is called CoWoS.

CoWoS stands for Chip-on-Wafer-on-Substrate. Hold onto that name, because by the end of this you will understand exactly what each word means, and why one of them is about to change.

---

First, the mental model of what packaging even is.

When people say "advanced packaging," they mean the art of taking several separate finished chips and joining them into one high-performance unit. There are roughly three tiers, in increasing intimacy.

The first tier is called fan-out. Imagine a chip whose electrical contacts are packed too tightly to connect directly to a circuit board. Fan-out places the chip on a carrier and builds a set of wiring layers that spread its connections outward, like an adapter, to a wider, more manageable pattern. Apple uses this for iPhone processors.

The second tier is called two-point-five D, and this is the one that matters for AI. Here, several active chips — a graphics processor and its memory stacks — sit side by side on top of a shared slab called an interposer. The interposer is the floor they all stand on, and its job is to carry an enormous amount of very fine wiring between them. This is how an Nvidia data-centre GPU talks to its high-bandwidth memory. T-S-M-C's version of two-point-five D packaging is CoWoS.

The third tier is full three-D, where active chips are stacked directly on top of one another, connected by vertical copper channels running straight through the silicon. That is the frontier, and it is how memory itself is built.

For the rest of this, we live in the second tier — the interposer.

---

Now, a crucial correction to a mistake almost everyone makes.

It is tempting to picture that interposer as just a blank slice of silicon, a passive tray. It is passive, in the sense that it does no computing — there are no transistors on it. But it is absolutely not blank. Etched across its surface are thousands upon thousands of microscopic wires, finer than anything on a circuit board, plus tiny copper channels punched vertically through it. The interposer is, in effect, an extremely high-resolution circuit board made of silicon. Its entire reason to exist is to carry wiring so dense that the graphics processor and the memory stacks can exchange data at staggering rates.

So keep three kinds of silicon straight in your head. The graphics die is silicon with logic etched on it. The memory is silicon with memory etched on it. And the interposer is silicon with only wiring etched on it. Passive is not the same as blank. That distinction is going to matter enormously later.

---

Why is the interposer made of silicon at all? Because, until very recently, silicon was the only material you could draw wiring that fine on. We already had the lithography machines — the same ones that pattern transistors — capable of drawing sub-micron wires. And that wiring density is the whole point: it is what delivers the bandwidth between processor and memory. So silicon it was.

But silicon comes with a hidden cost, and that cost is the heart of this entire story. To use silicon, you must use a wafer. And that leads us to the reticle limit.

Think of printing a poster on a home printer that can only handle a single sheet of A4 at a time. In chip-making, the equivalent is the reticle — the largest pattern the lithography machine can project in a single exposure. That window is fixed at twenty-six millimetres by thirty-three millimetres. Nothing patterned in one shot can be larger than that.

Now, an interposer for a modern AI package needs to be several times larger than that window, because the graphics processor and all its memory stacks have to sit on it together. The workaround is called reticle stitching: you expose the pattern in overlapping tiles, like taping A4 sheets together into a poster. But every seam is a chance for misalignment, and yields fall off a cliff as you add tiles. In practice you can reach maybe three-and-a-bit times the reticle area before it becomes unmanageable. The interposer has no transistors, remember — but it still needs a lithography stepper to draw its fine wiring, and that stepper still has that fixed projection window. Fine wiring means a stepper, and a stepper means the reticle limit. It does not matter whether you are drawing transistors or wires.

---

This reticle wall is exactly what forced the first big evolution: the move from CoWoS-S to CoWoS-L. And there is a subtle point here that trips everyone up, so let me be precise.

What changed between the two was not the chips. The graphics dies and the memory stacks were always separate pieces sitting side by side. What changed was the floor they stand on.

In CoWoS-S, the "S" for silicon, the floor is one big continuous sheet of silicon. Beautiful wiring, but reticle-limited in size, and expensive.

In CoWoS-L, the floor is mostly cheap organic material — essentially fancy circuit-board stuff — with small patches of silicon embedded into it only at the specific joints where two chips need to talk to each other at high bandwidth. The organic floor carries the coarse wiring, which does not need a lithography stepper and therefore has no reticle limit. The little silicon bridges carry the fine wiring, but only where it counts. It is like pinning a cheap corkboard to the wall and taping high-resolution photographs onto it only in the spots that need the detail.

That is the entire difference between S and L. And it is worth stressing this is not the same idea as chiplets. Chiplets means breaking the active compute chip into smaller pieces for cost and yield reasons. CoWoS-L means breaking the passive floor into pieces for size reasons. Different problem, different layer of the stack. You can mix and match them freely.

---

Let me put some economics on the table, because the cost structure tells you where the pain is.

For that Blackwell B200, the biggest single cost is not the processor and not the packaging — it is the memory. The high-bandwidth memory stacks account for roughly forty-five percent of the manufacturing cost, around twenty-nine hundred dollars. The packaging is about seventeen percent. Yield losses — the packages that fail and get scrapped — are another sixteen percent. The logic dies themselves, the part we think of as "the chip," are only about fourteen percent. Total manufacturing cost lands somewhere around sixty-four hundred dollars, and the thing sells for thirty to forty thousand. Memory dominates, packaging beats logic, and scrap is enormous. That is the new economics of an AI chip.

Why is scrap so high? Because this is genuinely hard to manufacture. Each die is bonded onto the interposer individually, under heat and pressure, and that takes seconds per bond with a dozen or more dies per package. The different materials — silicon, organic, mould compound — expand by different amounts when heated, so the whole assembly wants to warp, and warping was a major cause of the early Blackwell yield problems. Memory supply constrains everything even when interposer capacity exists. And testing a stack of a dozen chips, any one of which can kill the whole unit, is its own nightmare.

The scale of T-S-M-C's response is the reason the AI boom has kept pace at all. In late twenty twenty-three they could produce something like thirteen thousand CoWoS wafers a month. By the end of twenty twenty-six they are heading for a hundred and twenty to a hundred and thirty thousand. A tenfold increase in three years, and Nvidia alone books more than half of it.

---

I want to spend a moment on something that gives you a visceral feel for how extreme this engineering is: power delivery.

An H100 processor draws about seven hundred watts. Follow the electricity from the wall and watch what happens. It leaves the wall as household voltage, gets converted down to twelve volts, and at twelve volts, seven hundred watts means around fifty-eight amps — already like a beefy electric-vehicle charger. But the transistors need less than one volt. So a regulator drops the voltage from twelve volts to about zero-point-eight volts. And here is the thing about power: when voltage drops fifteen-fold, current rises fifteen-fold to compensate. At zero-point-eight volts, that seven hundred watts is now flowing as roughly eight hundred and seventy-five amps.

Eight hundred and seventy-five amps. For scale: a phone charger is two amps, a toaster is about eight, a household fuse trips at thirteen, an electric-vehicle charger is forty, an arc welder is two hundred. This chip pulls eight hundred and seventy-five — and it does so through connections thinner than a human hair.

How does it not simply melt? By splitting that current across as many parallel paths as physically possible. Thousands of solder balls under the package. Thousands of bumps above them. Thousands of vertical vias through the interposer. Tens of thousands of micro-bumps under each die. At every layer, the current fans out across a vast number of tiny parallel connections, because eight hundred and seventy-five amps down any single path would vaporise it. The recurring theme of this whole field is: divide and conquer the current.

There is a beautiful, maddening problem hiding in here called I-R drop. I times R — current times resistance — is the voltage you lose pushing current through anything that resists it. Every wire and via has a little resistance, so every one of them eats a sliver of your voltage budget. You have eighty billion transistors spread across a piece of silicon the size of a postage stamp, and every one of them needs to see very close to the same voltage. If one busy corner sags by even a few tens of millivolts, the transistors there switch a touch too slowly, miss the next clock tick, and the chip computes the wrong answer. Not an error message — just, quietly, the wrong answer. Engineers spend days running simulations that model current through every segment of the copper mesh, hunting for the one corner that sags, and then the fix is agonisingly local: widen this wire, add a via there, nudge a capacitor fifty microns to the left. Then simulate for days again.

---

And since we are marvelling, let me name the two most astonishing machines in the background, because they anchor just how deep this dependency chain goes.

The first is the E-U-V lithography scanner that patterns the finest features. It is a three-hundred-and-fifty-million-dollar, hundred-and-eighty-tonne machine, and to make its light it fires a laser at a falling droplet of molten tin — twenty-five microns across — fifty thousand times a second. The first pulse flattens the droplet into a pancake, the second vaporises it into a plasma hotter than the surface of the sun, and that plasma emits extreme-ultraviolet light. That light is gathered by mirrors polished so flat that if you scaled one up to the size of Britain, its biggest bump would be a millimetre tall. None of this existed in production fifteen years ago; serious people said it never would. Every AI chip in the world is patterned by a machine that runs on tiny exploding droplets of metal.

The second marvel is subtler. The features on a modern chip are far smaller than the wavelength of light used to print them. It is like painting a miniature portrait with a brush wider than the canvas. The light diffracts and blurs. So the mask is deliberately pre-distorted — warped, fragmented, with extra shapes added that appear nowhere on the final chip — so that after diffraction mangles it, the pattern lands on the wafer correctly. If you looked at a modern photomask, you would not recognise it as a chip. It looks like abstract art. Computing those distortions is one of the largest applications of computational physics in the industry. There is something recursive about it: chips are designed by software that computes how light bends through a mask so that light can pattern the silicon that runs the software that designs the next chip. The snake eats its tail at every level.

The point of naming these is the fragility underneath the boom. The AI revolution depends on T-S-M-C's transistors, which depend on those lithography machines, which depend on a particular grade of glass for their mirrors, and also on a specific build-up film that happens to be made by a company better known for food seasoning, and on the memory-makers' vertical-via etching, and on the copper chemistry in a handful of substrate cleanrooms. Pull any one of those threads and the whole thing stops.

---

Right. That is the foundation. Now the shift that this entire article has been building toward — and it turns on a single word in the name CoWoS. Chip-on-Wafer-on-Substrate. The word is Wafer.

There is a new approach coming, and its name changes exactly one syllable: CoPoS. Chip-on-Panel-on-Substrate. Wafer becomes Panel. That is the whole change. And to see why it is such a big deal, you have to understand where a wafer physically comes from, versus where a panel comes from — because they are born in completely opposite ways.

A silicon wafer is cut from a bigger round thing. You grow ultra-pure silicon into a single solid crystal cylinder — a boule, shaped like a fat salami, about three hundred millimetres across and a metre or two long. Then you slice that cylinder, like slicing salami, into thin round discs. Each disc is a wafer. It is round because the crystal is round. You do not choose the shape; you inherit it from the cylinder. And three hundred millimetres is not arbitrary either — it is the size the physics of crystal-growing and the entire tool ecosystem settled on decades ago. The industry tried to move to four hundred and fifty millimetres years back and largely gave up, because growing bigger flawless crystals is brutally hard.

A panel is the opposite. A panel is not sliced off a crystal at all. It is manufactured to size, as a flat rectangular sheet — think of a large pane of glass, or a large circuit-board-style laminate. Its shape and its size are a free engineering choice, because you are building a sheet rather than slicing a cylinder. Do you want it three hundred and ten millimetres square? Five hundred and fifteen millimetres square? Bigger? You simply build it that way.

So the fundamental contrast is this. Round is a slice of a grown crystal — the shape dictated by nature. Rectangular is a made-to-order sheet — the shape chosen by engineers. That one difference is the entire story of CoPoS.

---

Why does the shape matter so much? Two reasons, and a good way to feel both is to picture cutting cookies out of rolled dough.

With CoWoS, your dough only ever comes as a round disc, because it was sliced off that salami. Now try to cut square cookies out of a circle. Around the entire rim you get useless curved off-cuts — crescents of scrapped, extremely expensive silicon. And it gets worse the bigger each cookie is: a large package near the edge simply spills off into nothing. As AI packages balloon toward five and eight times the reticle area, those wasted crescents become enormous.

With CoPoS, you can roll the dough into any rectangle you like. Square cookies tile a rectangle with almost no waste at all. And the sheet can be far larger to begin with. A three-hundred-millimetre wafer has an area of about seventy thousand square millimetres. A five-hundred-and-fifteen-millimetre panel has nearly two hundred and sixty thousand — around three-and-a-half times the area, and it wastes far less of that area at the edges on top of being bigger. So panels win twice: less edge waste, and more room. You can also host packages so large they would never fit on a wafer at all.

Now, you might reasonably ask: if a panel is so much better, and glass is cheap, why on earth were we ever slicing expensive silicon in the first place? Weren't we trapped?

We were, but not out of foolishness. Remember, silicon was the only material you could draw that ultra-fine wiring on. The trap was never the silicon itself — it was the wafer format that silicon forces on you. Choose silicon, and you are stuck with round discs, a three-hundred-millimetre ceiling, and a high cost per unit of area, because chip-grade silicon is very expensive real estate to be using as a glorified wiring board.

Two things changed to spring the trap. First, glass and advanced organic laminates matured to the point where they can now carry wiring fine enough for most of the job — not quite silicon-fine everywhere, but close, and closing. Second, for the few spots that still demand silicon-grade density, you can embed one tiny silicon bridge just there, and use cheap panel for everything else — a postage stamp of expensive silicon where it counts, a big cheap sheet everywhere else.

And here is the key realisation. The moment your wiring no longer has to sit on silicon, you are free of the wafer entirely — free of the round shape, free of the size ceiling, free of the cost. That is the real unlock. Not "glass is magic." Rather: you have stepped off the crystal. And notice what we are actually swapping. We are not going from etched silicon chips to a square of glass — the chips on top do not change one bit. We are going from a silicon wiring-board to a glass wiring-board. That is all.

---

Finally, why this matters beyond the physics — because this reshuffles an entire industry.

Today, CoWoS is a chokepoint controlled by one company. Because it is silicon-wafer based, packaging capacity is tied directly to T-S-M-C's interposer-wafer lines, and that capacity is the single biggest constraint on how many top-end AI processors exist in the world. That is precisely why T-S-M-C has such pricing power and why everyone is supply-starved.

Panel packaging threatens to break packaging free of the silicon-wafer supply chain altogether. Panels are made on equipment much closer to circuit-board, substrate, and flat-panel-display manufacturing than to wafer fabs. And that opens the door to a whole cast of players who were never in the interposer game: substrate specialists like Unimicron, Ibiden, A-T-and-S, and Shinko; the big assembly-and-test houses like A-S-E, Amkor, and S-P-I-L; and glass and display-heritage names like Corning, and S-K-C's Absolics venture. The cost curve bends downward too, because panel tools spread their cost over three to four times more area per carrier with far less waste, which could genuinely de-bottleneck AI supply over the next few years.

Two important caveats, so you hold this at the right altitude. First, T-S-M-C is not sitting still — it is developing CoPoS aggressively itself, because it would far rather cannibalise its own CoWoS than be disrupted. So this may not democratise the industry as much as the optimists hope. Second, panels warp, and fine-line yield on panels is not yet at silicon parity, so high-volume CoPoS is a twenty twenty-seven-and-beyond story, not a today story. This is a multi-year structural shift to watch unfold, not a switch that flips.

So here is the whole thing in one breath. Packaging has quietly become the thing that gates AI compute. CoWoS — chip on wafer on substrate — is how we do it today, and its constraint is the round silicon wafer that its fine wiring is trapped on. CoPoS — chip on panel on substrate — keeps the exact same chips and the exact same recipe, and changes only the carrier underneath them, from a round crystal-slice to a rectangular made-to-size sheet. Squares tile rectangles. You escape the round shape, the size ceiling, and the cost. And in doing so, you might just loosen the tightest chokepoint in the entire artificial-intelligence supply chain.

We have been studying, in effect, the machine we are running on. And it is about to change shape.

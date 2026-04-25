# The Evolution of the Memory Cell: From Floating Gate to Stacked Charge Trap

## Why we needed non-volatile memory in the first place

To understand memory cells, start with the hole in the market they fill. By the late nineteen sixties, computer memory came in three flavours, all unsatisfactory.

Dynamic RAM, or D-RAM, stores each bit as charge on a tiny capacitor. It is fast and dense, but the capacitor leaks within milliseconds, so the entire memory must be refreshed thousands of times per second. Pull the plug and everything vanishes.

Static RAM, or S-RAM, stores each bit in a flip-flop made of six transistors. Faster than D-RAM, no refresh needed, but six transistors per bit makes it expensive. Still loses everything when power dies.

Read-Only Memory was non-volatile, but written once at the factory. You could not update it.

The dream was a memory that was non-volatile, electrically rewriteable, and dense enough to be cheap. That dream is what every story in this document is chasing.

## Nineteen sixty-seven: the floating gate is invented

At Bell Labs in nineteen sixty-seven, Dawon Kahng and Simon Sze proposed a beautifully simple modification to the standard transistor. Take a normal field-effect transistor — the workhorse of all modern electronics, with a control gate sitting above a channel that carries current between source and drain. Now insert a second gate between the control gate and the channel. Make it out of polysilicon, and crucially, surround it completely with silicon dioxide insulator. It connects to nothing.

This is the floating gate. Electrically isolated, it has no way for charge to escape under normal conditions. If you can get electrons onto it, they stay there for years. If you can pull them off, they stay off.

The intuition you already have — electrons in a bucket — is essentially correct. The bucket is a tiny piece of polysilicon, maybe a hundred nanometres across in the original devices, and the bucket walls are silicon dioxide, which is one of the best insulators humans know how to make. The bucket leaks, but slowly enough that data survives a decade.

How do you read the bit? When electrons sit on the floating gate, their negative charge repels other electrons in the channel below. This makes the transistor harder to turn on — its threshold voltage shifts higher. To read, you apply a moderate voltage to the control gate. If the transistor conducts, the bucket is empty. If it does not, the bucket is full. One bit.

How do you write? You apply a high voltage that forces electrons through the supposedly impenetrable oxide and onto the floating gate. There are two physical mechanisms in play. Hot-electron injection accelerates electrons in the channel until they have enough energy to leap the oxide barrier. Fowler-Nordheim tunnelling uses a strong electric field to make electrons quantum-mechanically tunnel through the oxide. Erasing reverses the field and pulls electrons back off.

Every program-erase cycle abuses the oxide a little. After enough cycles — originally a few thousand, today as low as a few hundred for the densest cells — the oxide breaks down and the cell fails. This is the endurance problem, and it has shaped every architectural decision that follows.

## Nineteen seventy-one to nineteen eighty: from EPROM to flash

Intel commercialised the first floating-gate memory in nineteen seventy-one. Dov Frohman, a young Intel engineer, built the EPROM — Erasable Programmable Read-Only Memory. You wrote it electrically, but to erase it you had to expose the chip to ultraviolet light. UV photons knock electrons off the floating gate. This is why old EPROMs had a little quartz window on top of the package: to let the UV in. If you have ever seen a vintage chip with a circular glass window, that is what you were looking at.

In nineteen seventy-eight, George Perlegos at Intel built the first EEPROM — Electrically Erasable Programmable Read-Only Memory. Each cell now had its own erase mechanism. No more UV lamp. But each cell needed extra transistors for byte-level erase, which made EEPROM expensive and low-density.

Then in nineteen eighty, Fujio Masuoka, a Toshiba engineer, made the breakthrough that turned this into a trillion-dollar industry. He realised that if you gave up byte-level erase and only allowed erasing in large blocks, you could throw away most of the per-cell circuitry. The cell became tiny. The chip became cheap. The trade-off was that to update one byte, you had to read out and rewrite a whole block.

He named the result flash memory because erasing a block reminded him of a camera flash. Toshiba famously did not appreciate what he had invented and paid him a small bonus. He later sued and got a settlement of around eight hundred thousand dollars, against an industry he had personally created which is now worth more than half a trillion dollars annually. The episode is a small monument to corporate myopia.

## Nineteen eighty-eight: the NAND-NOR fork

Flash memory split into two architectural families.

NOR flash, which Intel commercialised first in nineteen eighty-eight, wires its cells in parallel, like a logical NOR gate. Every cell is directly addressable. You can read any byte in nanoseconds, and you can even execute code directly out of NOR memory — what is called execute-in-place, or X-I-P. The downside is that the parallel wiring eats area. Density is poor.

NAND flash, which Toshiba shipped in nineteen eighty-nine, wires its cells in long series strings, like a logical NAND gate. Originally sixteen cells per string, now over two hundred. Series wiring is dense — you have far fewer wires per cell — but you can no longer read a single cell directly. You have to activate the whole string and read out a page at a time, typically several kilobytes.

These trade-offs sorted the two technologies into different markets. NOR flash became the home of code storage: BIOS chips, embedded firmware, the boot ROM in your phone. NAND flash became the home of mass storage: USB sticks, S-D cards, and eventually solid-state drives. By raw bits shipped, NAND outsells NOR by something like a hundred to one. NOR is the niche; NAND is the empire.

## The clever insight: storing more than one bit per bucket

For the first two decades of flash, each cell stored one bit. Either the floating gate held electrons or it did not. This is called Single-Level Cell, or S-L-C.

Then someone had a better idea. The floating gate does not have to be binary. It can store a *quantity* of electrons. Different quantities create different threshold voltages. If you can reliably distinguish four different voltage levels, you have stored two bits in one cell. Eight levels gets you three bits. Sixteen levels, four bits.

The progression went like this:

Single-Level Cell stores one bit per cell, two states, around one hundred thousand program-erase cycles of endurance. Used in enterprise and industrial applications where reliability matters more than cost.

Multi-Level Cell, M-L-C, stores two bits per cell, four states, around ten thousand cycles. The mainstream consumer SSD of the early twenty-tens.

Triple-Level Cell, T-L-C, stores three bits per cell, eight states, around three thousand cycles. Most consumer SSDs today.

Quad-Level Cell, Q-L-C, stores four bits per cell, sixteen states, around one thousand cycles. Cheap bulk storage and increasingly hyperscaler workloads.

Penta-Level Cell, P-L-C, stores five bits per cell, thirty-two states, with endurance under five hundred cycles. Mostly research with very limited commercial deployment, because the trade-offs become brutal.

The trade-off: each extra bit doubles the number of voltage levels you have to distinguish. The "windows" between levels shrink. Smaller windows mean noisier reads, which means more aggressive error correction, which means slower writes that have to make multiple programming passes to land voltages in narrower targets. Endurance falls because each cycle has to nudge the voltage with greater precision, and the oxide cannot tolerate that abuse for long.

There is a deep insight here: NAND has been getting denser not just by shrinking cells, but by raising the *information density per cell*. The same physical bucket now holds four or five bits instead of one. We have been mining the same physical structure for ever-more bits, on top of geometric scaling.

## The wall: why planar floating gate stopped working

By around twenty thirteen to twenty fifteen, planar two-dimensional NAND scaling hit a wall and essentially stopped. Four physical problems converged.

First, electron count. As cells shrink, the floating gate gets smaller and holds fewer electrons. A planar floating gate at twenty nanometres holds maybe a few hundred electrons total. At fifteen nanometres, perhaps a hundred. To distinguish sixteen voltage levels, as Quad-Level Cell requires, you are trying to count tens of electrons. At that scale, quantum noise — single electrons coming and going — becomes catastrophic.

Second, cell-to-cell interference. Adjacent floating gates couple capacitively to each other. Programming one cell shifts the apparent stored state of its neighbours. The closer the cells, the worse this coupling. At the smallest planar nodes, neighbour coupling rivalled the actual stored signal.

Third, oxide wear. Thinner cells need thinner tunnel oxides for the right electric fields. Thinner oxides wear out faster. Endurance was falling off a cliff.

Fourth, lithography cost. To go below fifteen nanometres planar would have required extreme ultraviolet lithography, or E-U-V, before E-U-V was actually ready, and at a per-wafer cost the NAND industry's commodity economics could not support.

The whole industry hit this wall at roughly the same time. Planar NAND essentially stopped scaling. The replacement was not a smaller version of the same thing. It was a different cell, and a different geometry.

## The bucket changes material: charge trap flash

Before the geometry could change, the cell itself had to change. The story here is the rise of charge trap flash, often abbreviated C-T-F. The structure had been known since the nineteen seventies as SONOS — Silicon, Oxide, Nitride, Oxide, Silicon — but it had been a curiosity, not a mass technology.

The idea: instead of storing electrons on a *conducting* polysilicon island, store them in a *non-conducting* silicon nitride layer. Each electron occupies a discrete trap site within the nitride. The electrons are not free to move around within the layer. They sit where they land.

This sounds like a small change. It is enormous. Consider what happens when a defect appears in the tunnel oxide — a tiny pinhole leak path. A floating gate is conducting, so all of its trapped electrons can flow to that one defect and escape. One pinhole drains the whole bucket. A charge-trap layer is non-conducting, so only the electrons sitting near the defect leak out. The rest stay put.

This makes charge trap flash dramatically more defect-tolerant than floating gate flash. And defect tolerance, as we are about to see, is the precondition for stacking.

## Twenty thirteen: the pivot to the third dimension

In twenty thirteen, Samsung shipped the first commercial three-dimensional NAND, branded V-NAND. Toshiba had published the underlying concept, called Bit Cost Scalable or BiCS, back in two thousand seven, but Samsung was first to volume manufacturing.

The insight is so simple it feels like cheating. Instead of fighting to shrink cells horizontally, *rotate the cells ninety degrees and stack them vertically*. The cells themselves can be relatively large — modern three-dimensional NAND uses nodes around thirty to forty nanometres, far more relaxed than the leading-edge planar NAND it replaced. You get density not from shrinking but from stacking.

The architecture is worth understanding because most explanations skip it.

Step one: build a stack of alternating conductor and insulator layers on a silicon wafer. A modern stack might be over two hundred such layer pairs.

Step two: drill vertical holes — called memory holes — straight down through the entire stack. These holes are perhaps eighty to a hundred nanometres in diameter and thousands of nanometres deep. Drilling them is one of the hardest things humans currently do at industrial scale.

Step three: line each hole with the gate stack. From outside in: a blocking oxide, the silicon nitride charge trap layer, a tunnel oxide, and finally a polysilicon channel running down the middle.

Step four: each conductor layer in the original stack now becomes a word line — a horizontal control gate that wraps around every memory hole that passes through it. Each vertical channel becomes a string of cells, with one cell formed wherever the channel passes through a word line.

So a one-hundred-and-twenty-eight-layer three-dimensional NAND chip puts one hundred and twenty-eight cells in the footprint of one. You have gone from areal density to volumetric density.

This is also why charge trap flash was a prerequisite for three-dimensional NAND. Floating gates need conductive polysilicon islands, which are very hard to deposit reliably as discrete pieces down a high-aspect-ratio hole. Silicon nitride deposits as a continuous, conformal coating along the entire hole. The materials change in the previous section is what enabled the architectural change in this one. They are one story, not two.

## Where the technology stands in twenty twenty-six

Layer counts are now well over two hundred and climbing. Samsung, S-K Hynix, Micron, and Kioxia with Western Digital are all shipping products in the two-hundred-to-three-hundred-layer range, with public roadmaps to five hundred and beyond by the end of the decade.

Above roughly ninety-six layers, etching one continuous memory hole becomes physically impossible — the hole walls go out of alignment, or the etch chemistry stops reaching the bottom. So manufacturers etch about ninety-six layers, deposit a tier, then etch another ninety-six on top, and align the two tiers. A "two-hundred-and-thirty-two-layer" chip is often two one-hundred-and-sixteen-layer tiers stacked. This is called string stacking, or sometimes a deck architecture.

The peripheral logic — decoders, sense amplifiers, charge pumps — used to sit alongside the memory array, wasting precious die area. Two architectural innovations have improved this. CMOS-under-array, abbreviated CuA, builds the logic directly underneath the memory stack. CMOS-bonded-array, CBA, builds the logic on a separate wafer optimised for logic and hybrid-bonds it onto the memory wafer afterwards. Both significantly improve effective density and let logic and memory be optimised on different process nodes.

Quad-Level Cell is now mainstream for consumer S-S-Ds and is increasingly being adopted by hyperscalers for bulk storage. Penta-Level Cell exists in samples but the endurance and write-speed trade-offs have kept it out of volume. On a total-cost-of-ownership basis, NAND flash has now crossed below hard-disk-drive cost for many workloads, and the long-predicted collapse of the H-D-D market is finally starting to look credible. Pure Storage made that bet publicly.

## The graveyard: emerging memories that did not make it

For thirty years, the holy grail has been a memory that is faster than NAND, denser than D-RAM, non-volatile, and cheap enough to compete. None of the contenders has made it to volume. A brief tour of the graveyard:

Phase Change Memory, P-C-M, stores bits as crystalline versus amorphous phases of a chalcogenide alloy of germanium, antimony, and tellurium. Heat the alloy briefly and it crystallises. Heat it more and quench, and it freezes amorphous. The two phases have very different electrical resistance. Intel commercialised this as 3D X-Point, branded Optane, jointly with Micron. It was the closest anyone has come to a true storage-class memory — sitting between D-RAM and NAND in latency. Intel killed the product line in twenty twenty-two. It could not beat D-RAM on price or NAND on density. The technology was real and elegant; the economics did not work.

Magnetic R-A-M, M-R-A-M, stores bits in magnetic tunnel junctions whose resistance depends on the alignment of two magnetic layers. The current variant, Spin-Transfer Torque M-R-A-M or S-T-T M-R-A-M, is shipping today as embedded memory inside microcontrollers, replacing the embedded flash that microcontroller fabs are increasingly unable to manufacture below twenty-two nanometres. M-R-A-M is excellent at this niche but standalone density is poor and it will not replace D-RAM or NAND.

Resistive R-A-M, ReRAM or R-R-A-M, forms and breaks conductive filaments inside a metal-oxide layer. It has been "five years away" for fifteen years. Some niche commercial use exists. The mainstream breakthrough has not come.

Ferroelectric R-A-M, FeRAM, switches the polarisation of a ferroelectric crystal. Old technology, used in tiny niches like smart cards and industrial instruments. Recent interest in ferroelectric hafnium oxide may give it new life as embedded memory.

The pattern is consistent. Each emerging memory is excellent on one or two axes — speed, endurance, retention — but loses on cost. NAND's manufacturing learning curve over thirty years is a moat that no challenger has crossed.

## Why this matters for an investor

A few things follow from the above.

NAND is a brutal commodity cycle with four global players: Samsung, S-K Hynix together with Solidigm, Micron, and Kioxia together with Western Digital. Capacity decisions take years to come online and the market over- and under-supplies in roughly two-year cycles.

Three-dimensional NAND scaling is fundamentally a capital-equipment story rather than a lithography story. The hard parts are etching and deposition — wells dug deeper, walls coated more uniformly. The big winners on the equipment side are Lam Research and Applied Materials in the United States, and Tokyo Electron in Japan. ASML's E-U-V, which dominates the leading-edge logic conversation, is much less central to NAND.

D-RAM is the opposite. D-RAM is hitting the lithography wall now, requiring E-U-V for the smallest cells. The hottest D-RAM sub-story is High-Bandwidth Memory, H-B-M, which stacks D-RAM dies on top of a logic base die and ships them inside A-I accelerators. S-K Hynix is currently leading H-B-M; Samsung is catching up; Micron is third.

The emerging memories are mostly venture graveyards. A handful — embedded M-R-A-M, ferroelectric hafnium oxide — have found niches. None will displace NAND or D-RAM for general-purpose storage in the foreseeable future. The real action remains layer-count scaling in NAND and H-B-M scaling in D-RAM. If you only have time to track two technical metrics in memory, those are the two.

## Closing intuition

The pithy version of all of this: we started with a leaky bucket of electrons surrounded by glass. We made the bucket smaller until it stopped working. We changed the bucket from a piece of metal to a piece of insulator so it was no longer all-or-nothing leaky. Then we stopped making it smaller and started stacking copies of it on top of each other, hundreds deep. And along the way we learned to read not just whether the bucket was full or empty but how full it was, to four bits of precision.

The whole story is best told as a sequence of physical limits hit and architectural innovations to escape them. Every dead end produced a different cell, a different material, or a different geometry. The rough edges of physics — quantum noise, oxide wear, defect statistics, etch aspect ratios — wrote the script.

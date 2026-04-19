# Advanced Packaging, From First Principles

This is a ground-up rebuild of a topic that most sources handle badly: how modern chips are packaged. By packaged I don't mean shipping boxes. I mean the plumbing that connects multiple pieces of silicon together inside a single device. If you've read about CoWoS, EMIB, Foveros, SoIC, or hybrid bonding and found the explanations chaotic, this piece tries to fix that by reorganising the whole field around a single axis. It exists as a written document with six diagrams. I'll cue you when we reach each one so you can pull up the PDF if you want to stare at it. Otherwise, it's built to flow entirely by audio.

Here's the central claim. Every packaging technology, old and new and unreleased, is a different way to trade cost against interconnect density. Once you hold that axis in your head, all the brand names collapse into points on a single ladder. No prior knowledge is assumed beyond: a chip is a piece of silicon with transistors on it.

## Part one. Why advanced packaging exists

Advanced packaging is recent as a commercial priority. Really the last five years. For most of the transistor era, nobody cared how chips were packaged, because chips themselves were improving so fast that packaging overhead looked negligible. Two things changed that simultaneously.

### The transistor cost crisis

Moore's Law has two limbs. Transistor density doubles every two years, and, this is the economic part, transistor cost halves at the same rate. For decades both held together. The density limb still mostly works. A five nanometre transistor really is smaller than a seven nanometre transistor. But the cost limb broke around the introduction of FinFETs, roughly ten years ago.

A few numbers to make this concrete. A TSMC N7 wafer costs roughly nine and a half thousand dollars. A TSMC N5 wafer costs roughly sixteen thousand dollars. Transistors per square millimetre improved maybe one point eight times between those two nodes. Do the arithmetic: cost per transistor actually got worse at five nanometre.

Three compounding reasons. EUV lithography is expensive. Each new node uses about thirty-five percent more process steps than the previous one. And yield suffers as dies get larger, because defect density per square millimetre is roughly constant. A single defect kills a more expensive chunk of silicon when the die is bigger.

The implication is simple and nasty. You can no longer get cheaper by moving to a newer node. You get more performance per square millimetre, but each square millimetre costs more. The old strategy of wait two years, port to the next node, watch costs fall, stopped working.

### The I/O crisis

The second crisis is about connections. A chip is not just transistors. It is also pads, the electrical contacts where signals and power enter and leave the die. Pads sit on the die's surface, each taking a minimum area set by something called bump pitch: the centre-to-centre spacing of the solder contacts.

Here is the historically painful number. Flip-chip bump pitch went from about two hundred microns in the nineteen nineties to about one hundred and thirty microns by the twenty tens. That's roughly a two-times improvement in bump density. In the same window, transistor density improved by about two thousand times.

There's a chart in the written version here plotting these two curves over time. Transistors per die ride up sharply through three orders of magnitude. I/O bumps per die barely budge. The takeaway is just that: a three-orders-of-magnitude gap has opened between how fast the logic can shrink and how fast the plumbing can shrink.

The practical effect is that a modern chip's floor plan often looks like a small logic region surrounded by a huge ring of bump pads. The logic could shrink to the next node, but the pad ring can't, because the package can't handle any finer pitch. So the die stays artificially large, and the expensive new node doesn't buy you a smaller die. It buys you extra silicon you didn't want. This condition is called pad-limited.

Pad-limiting is the fingerprint of the whole advanced packaging problem. Everything the industry has invented, fan-out, interposers, bridges, TSVs, hybrid bonding, is some way of breaking the pad pitch floor.

### The reticle wall

There's a third ceiling, harder than either of the first two. ArF excimer lithography uses a reticle of fixed maximum size: thirty-three millimetres by twenty-six millimetres, for a total of eight hundred and fifty-eight square millimetres. That is the biggest area you can expose in a single lithography shot. You can draw a larger layout, but you cannot pattern a die larger than that in one exposure.

Nvidia's datacentre GPUs have been bumping against the reticle limit for about five years. The H100 is eight hundred and fourteen square millimetres. The A100 was eight hundred and twenty-six. You literally cannot buy a bigger monolithic logic die from TSMC.

Even if you could, yield punishes you. Defects per die scale linearly with die area. An eight-hundred-square-millimetre die gets about eight times as many defects per die as a one-hundred-square-millimetre die. Good dies per wafer fall faster than area increases. Large dies are a yield penalty on top of a cost penalty.

### The workload shift

Two crises walked in from the transistor side. A third, bigger one, walked in from the workload side. Chips stopped being just CPUs.

An Apple A15 or M2 is, by area, mostly not CPU. The CPU cores are a small fraction. The rest is cache SRAM, image signal processor, video codec blocks, neural engine, graphics, memory controllers. The workloads Apple ships that silicon for, camera, machine learning inference, media, screen, don't benefit much from general-purpose CPU cores.

Scale this up. A Google TPU is mostly a big systolic array of multipliers plus a wall of SRAM. An Amazon Trainium is a similar story. A Tesla Dojo training tile is almost entirely custom compute plus on-die memory plus an enormous bandwidth fabric. A Nvidia H100 is logic plus eighty gigabytes of high-bandwidth memory sitting in the same package.

The generalisation: modern workloads, AI, imaging, networking, recommendation, want a heterogeneous mix of silicon types. Logic at the most aggressive node. SRAM at an older, cheaper node, because SRAM stopped scaling at five nanometre. DRAM in its own special process. Maybe photonics or analog RF on top. These processes are mutually incompatible. You cannot fabricate them on the same die.

So you need a way to have them all live together in the same package.

### The chiplet resolution

Put the three crises together and you get a forcing function. Transistors don't get cheaper, so you cannot afford to put things that don't need the latest node on the latest node. Dies can't get much bigger, so the next generation of compute has to come from more silicon per package, not a bigger single die. And workloads want a mix of process types.

The answer is chiplets. Take what used to be a monolithic die, break it into smaller pieces on different processes, and re-assemble them inside a single package.

The benefits are straight arithmetic. Small dies yield better. Older processes for I/O and SRAM cost less. Designs can be reused across SKUs. AMD famously covered three market segments with three chiplet types, where Intel needed five monolithic designs. You can put more compute than fits in a reticle into one package.

The cost, and this is the whole subject of this piece, is that you now have to connect the chiplets. Connections between dies have historically been one hundred to one thousand times worse than connections within a die, along three axes: density, energy per bit, and latency. Every off-die hop costs enormous tax.

So the one-sentence summary. Advanced packaging is the project of making between-die connections approach within-die connections. Everything else is just the methods, and where each method sits on the single axis that matters: interconnect density.

## Part two. The single axis that organises everything

### Bump pitch is the master variable

Hold one number in your head: pitch. The centre-to-centre distance between adjacent electrical contacts at some interface. Measured in microns.

Density scales as one over pitch squared. Halving the pitch gives you four times as many connections in the same area. Everything in advanced packaging is, in the end, about driving pitch down.

There's a chart in the written version plotting the ladder of pitches across the packaging stack, on a log scale. Let me walk you through the approximate numbers. Top row, widest pitch: BGA balls, the big solder balls at the bottom of a package that connect it to a printed circuit board, about eight hundred microns. Then C4 flip-chip bumps, die to organic substrate: one hundred and fifty to two hundred microns. Fan-out RDL bumps: sixty to ninety microns. Silicon-interposer microbumps, used in CoWoS: forty to fifty-five microns. Intel Foveros microbumps: thirty-six to fifty microns. High-bandwidth memory stack microbumps: twenty-five to thirty-six microns. Then a jump to hybrid bonding for logic, like AMD V-Cache: under ten microns. And at the very bottom, Sony's image sensors have demonstrated hybrid bonding at zero point seven microns, finer than anything in the logic world. From top to bottom, about six orders of magnitude of density improvement.

Every advanced packaging technology is a way of achieving some row on this ladder at some cost. The lower you want to go, the more exotic and expensive the process. CoWoS, EMIB, SoIC are just brand names for specific ways of reaching specific rows.

### The dimensionality axis

Running perpendicular to the pitch axis is a second axis: how the chips are physically arranged relative to each other. This is what two-D, two-point-five-D, and three-D refer to. It's a separate dimension and it gets conflated with density constantly.

Two-D means chips lie flat next to each other on an organic substrate, with wires between them running through the substrate.

Two-point-five-D means chips lie flat next to each other on top of a passive silicon slab, called an interposer. Wires between them run through the interposer, which, because it's silicon, can carry much denser wiring than organic substrate. The interposer then connects downward to the organic substrate through another set of bumps.

Three-D means chips are stacked vertically. Active silicon sits on active silicon. Signals travel up and down through the silicon itself, through structures called through-silicon vias, or TSVs, or through direct copper-to-copper bonds.

There's a diagram in the written version with three side-by-side cross-sections showing two-D, two-point-five-D, and three-D layouts. The takeaway: two-point-five-D is literally about adding a passive silicon interposer layer. It's not an intermediate density level. It's a separate architectural choice.

A quick aside. When you read about two-point-one-D versus two-point-three-D in a trade article, silently translate to: organic substrate with extra lithographic routing, or organic substrate with a silicon bridge embedded. The point-something-D terminology tells you nothing useful about the actual structure, and nothing at all about density, which is the axis that matters. Always go back to pitch.

### The ladder of interconnect

Now the payoff. Every significant commercial packaging technology sits on one of seven rungs of what I'll call the interconnect ladder. Here it is, coarsest to finest.

Rung zero, wire bond. Gold or copper wires run from pads on the die edge up to lead frames on the package. Fifty to one hundred microns pitch along the die edge only. Used on memory, power management, analog. Not really an advanced packaging technology.

Rung one, flip-chip on organic substrate. The die is flipped active-side down. C4 solder bumps join die pads to an organic laminate substrate. Underfill is injected to lock them in. Pitch: one hundred to two hundred microns. The substrate is copper core plus Ajinomoto Build-up Film, known as ABF, the same material used in every modern desktop CPU. This is the baseline. A packaged chip means this unless someone specifies otherwise.

Rung two, fan-out, sometimes called FOWLP, wafer-level fan-out. Eliminate the substrate. Embed the bare dies in an epoxy mould compound, then pattern redistribution layers, thin-film copper wires on polymer, directly on top of the mould, fanning out to a wider array of external bumps. Pitch: sixty to ninety microns. Cheaper than Rung one for small packages because there's no separate substrate to buy. TSMC calls its fan-out InFO, short for integrated fan-out. ASE calls theirs FoCoS, Amkor calls theirs WLFO, Samsung calls theirs FOSiP. Apple A-series and M-series chips live on this rung.

Rung three, silicon bridge in substrate. Take an organic substrate, but carve a small cavity in it, and embed a tiny piece of silicon patterned with fine wiring. Two dies above the cavity talk to each other through this silicon bridge, which gives silicon-class density only where needed, at the die-to-die interface. Everywhere else the package stays cheap organic. Intel's EMIB, Embedded Multi-die Interconnect Bridge, is this. ASE's FOEB is a fan-out variant with a glass carrier. TSMC's InFO-LSI is another fan-out variant. The appeal: cheaper than a full silicon interposer, denser than plain fan-out, and no reticle limit because you can scatter many bridges across a big package.

Rung four, silicon interposer. A large slab of passive silicon, usually a few thousand square millimetres, stitched across multiple reticles, sits under all the dies. The silicon has fine copper wiring patterned on its top surface for die-to-die connections, and TSVs through its body to pass signals and power down to an organic substrate below. Pitch to the dies above: forty to fifty-five microns. Used by every high-volume AI GPU with high-bandwidth memory: Nvidia A100 and H100, Google TPU v4 and v5, Amazon Trainium, Intel Gaudi. TSMC calls this CoWoS-S. Samsung calls it I-Cube.

Rung five, three-D active stacking with TSVs and microbumps. Go vertical. Thin a die down to thirty microns or less. Drill TSVs through it. Put microbumps on both faces. Bond it face-down to another die. Signals now travel straight up through the stack. This is how HBM, high-bandwidth memory, is built, a base logic die with eight or twelve DRAM dies stacked on it. It is also how Intel Foveros works, a base die with logic dies stacked on top. Pitch: twenty-five to fifty microns. Because the stack is vertical, you can't easily use solder reflow to bond it. You need something called thermocompression bonding, which I'll explain in Part four.

Rung six, three-D hybrid bonding. Eliminate the bumps entirely. Polish the two mating silicon surfaces to near-atomic flatness. Bring them together in a clean environment. The copper pads on each surface fuse directly to the copper pads on the other, through metal diffusion at modest temperature. No solder, no underfill, no gap. Pitch: under ten microns for logic. Sony's image sensors have demonstrated zero point seven microns. TSMC brands its hybrid bonding as SoIC. That's what the CPU-to-SRAM bond in AMD's three-D V-Cache uses. Intel brands it Foveros Direct. Samsung brands it X-Cube. The Chinese NAND maker YMTC uses it wafer-to-wafer for their XStacking process. Sony's stacked image sensors were first to market.

There's a ladder diagram in the written version showing all seven rungs as cross-sections, with typical products labelled on each one. The visual shorthand: the higher up the ladder, the denser the interface, and the more exotic the process. Each rung up costs more and delivers more bandwidth per square millimetre of interface.

The industry's job, the last decade of innovation, has been to push the cost curve leftward, so that rungs that used to be unaffordable become affordable for merchant products.

## Part three. Substrates, RDL, and TSVs

Before we go deeper, let me walk through the common layers that show up across every rung.

Every package has a stacked hierarchy of layers. Top to bottom. The die, the piece of silicon with transistors. Near-die interconnect, microbumps, copper pillars, or direct bond. An interposer or bridge, if any. A fan-out RDL, if any. An organic substrate, a laminate of copper-clad core plus ABF, typically four to twenty layers thick, present in every non-wafer-scale package. BGA balls, big solder balls that connect the finished package to a PCB. And finally the PCB itself, the system board.

### ABF

ABF, Ajinomoto Build-up Film, deserves a paragraph. It's a thin polymer sheet produced by the Japanese company Ajinomoto. Yes, the monosodium glutamate company. The film was originally an industrial byproduct. Every modern flip-chip substrate laminates alternating layers of ABF and copper around a central glass-fibre core. The line-and-space width achievable on ABF is about ten microns today, with experimental coreless variants getting down to three to six microns.

ABF supply has been a real constraint. Ajinomoto is the dominant producer. When AI-GPU packaging demand exploded in twenty twenty-three, ABF allocation became a back-channel determinant of accelerator supply. Which is a reminder that a thirty-micron polymer film sitting under a thirty-thousand-dollar GPU is load-bearing infrastructure.

### RDL

RDL is shorthand for redistribution layer. Thin-film copper wires patterned lithographically on a polymer dielectric. Three or four layers are typical in a standard fan-out package. TSMC's InFO-SoIS, used for high-end networking silicon, goes up to fourteen RDL layers.

The key parameter is line-and-space, or L-S. The width of the copper wire and the gap between adjacent wires. Two microns L-S means two-micron wires with two-micron gaps, about two hundred and fifty wires per millimetre.

Rough frontier. Standard ABF is around ten microns L-S. Coreless ABF research from Cisco and Unimicron gets to six or even three microns. Advanced fan-outs like AMD RDNA 3 and MediaTek networking run at two microns. EMIB bridges started at five microns and are moving toward two. At the very edge, Amkor's SLIM technology hits zero point four microns, first layer only. And ASE's SPIL subsidiary hits zero point five microns with NTI. That high-density cluster, SLIM, NTI, next-generation EMIB, is asymptotically approaching silicon-interposer density for the fraction of the package that cares.

### TSVs

A TSV, through-silicon via, is a copper cylinder drilled vertically through a silicon wafer. It turns silicon into a substrate. Signals can pass through it rather than just across it. TSVs show up in three places. Silicon interposers connecting to the organic substrate below. DRAM dies in an HBM stack connecting to each other. And Intel Foveros base dies passing signals up through to top logic dies.

Typical diameter is five to ten microns. Pitch: seventeen to forty microns. Building them requires the same fab equipment as logic itself. Deep reactive-ion etch, copper electroplating, chemical-mechanical polish. That's commercially important. Only a fab can build a TSV. OSATs, outsourced assembly and test houses like ASE, Amkor, SPIL, can assemble around existing TSV-patterned silicon, but they cannot make the silicon itself. Which is why TSMC's packaging business is a fab business. And why Intel's foundry packaging arm is a competitive lever Intel likes, because Intel can make TSVs in-house.

### Chip-first versus RDL-first

There's a build-order question with real economic consequences. Chip-first: place the bare dies on a carrier, overmould them in epoxy, then pattern RDL over the top. Simpler, cheaper. But if the RDL has a defect, you've already committed good dies to it. Good die plus bad substrate equals waste.

RDL-first, also called chip-last: build the RDL and substrate first, test it, then bond the dies. Known-good substrate before you commit the dies. Harder, more expensive, but avoids the yield trap.

TSMC's InFO is chip-first. CoWoS is RDL-first. Most AI-class products need RDL-first because the substrates are big and complex enough that yield losses on them are non-negligible, and the dies going on top cost thousands of dollars each. For mobile applications like Apple A-series, chip-first InFO is fine because the packages are smaller and the dies cheaper.

### Reticle stitching

One more wrinkle. An interposer made from a single reticle exposure is capped at eight hundred and fifty-eight square millimetres. Modern AI packages need much more. H100's full interposer is around twelve hundred square millimetres. Blackwell's is roughly three times reticle. The trick is reticle stitching: expose the interposer with multiple reticle shots, carefully aligned so wiring crosses reticle boundaries without breaking. TSMC pioneered three-times reticle interposers for CoWoS. It is non-trivial and remains a technical moat.

## Part four. The bonding-method ladder

Cross-cutting the interconnect-density ladder is a second technical axis: how you actually join two surfaces together. There are three generations. Each rung of the interconnect ladder tends to force a specific bonding generation.

There's a three-panel diagram in the written version showing the three bonding methods side by side: mass reflow, thermocompression bonding, and hybrid bonding. Let me walk you through each.

### Mass reflow

The classical method. Place many dies on a substrate robotically, at three thousand to ten thousand dies per hour per tool. Run the whole assembly through a reflow oven, a conveyor that heats everything to about two hundred and fifty degrees Celsius. Melt the solder bumps. Let them bond to the pads. Cool down. Inject underfill. Cure. Fast, cheap, high-throughput. Works for C4 bumps at Rung one pitches and most fine-pitch flip-chip. Tool cost: around four hundred and fifty thousand dollars.

The problem: at microbump pitches, under fifty microns, two things break. First, warpage. Different materials have different coefficients of thermal expansion. Heating the whole assembly to reflow temperature warps the die and substrate differently. And when the solder freezes, the joints are uneven. Some bumps contact, others don't. Second, voids. Oxidation on the solder can leave tiny bubbles in the joint. At one hundred microns pitch, a small void is inconsequential. At twenty-five microns pitch, it's a dead connection.

Above some density, mass reflow simply stops working. AMD's Fiji GPU in twenty fifteen and some early interposer products got burned by exactly these failure modes.

### Thermocompression bonding

TCB. The next rung. Instead of heating everything in an oven, TCB places one die at a time with a tool head that applies three things: local heat, just the die being placed, not the whole substrate; mechanical pressure, forcing the bumps to deform into good contact; and sometimes ultrasonic vibration, which breaks the oxidation layer on the solder so clean metal meets clean metal. The die is held in place while the joint forms, then the head lifts. Cycle time: a few seconds per die. Throughput: five hundred to one thousand dies per hour, so three to ten times slower than reflow. Tool cost: around one and a quarter million dollars, almost three times more.

Why bother. Because the warpage goes away. The substrate stays cool. Only the local joint sees thermal stress. Bonds are void-free and gap-variation-free. Twenty-five-micron pitch becomes reliable.

Who uses TCB. Intel is by far the heaviest adopter, with around three hundred tools today, doubling with a new Malaysia facility. Intel's entire architectural strategy, EMIB, Foveros, Foveros Omni, depends on TCB reliability. And they've been co-developing TCB with tool vendors for a decade. TSMC uses TCB only for HBM stacking, not for their logic products. Their logic packaging is InFO-based and stays with mass reflow where possible. All HBM vendors, Samsung, SK Hynix, Micron, use TCB for HBM3's twelve-die stacks with thirty-micron dies. You simply cannot reflow-bond a stack that thin.

Tool vendors to know: BE Semiconductor, usually called Besi. ASM Pacific Technology, ASMP. And Kulicke and Soffa, K and S. Each has a slightly different niche. ASMP dominant in mobile package-on-package. K and S strong in HBM-style placements. Besi picking up the high-end Intel-style mixed-pitch work. TCB tool orders are a leading indicator of advanced packaging volume. Worth tracking from an investment perspective.

### Hybrid bonding

Skip solder entirely. The two mating surfaces are finished with a dielectric, usually silicon dioxide, in which copper pads are embedded flush with the surface. Both surfaces are polished to near-atomic flatness using chemical-mechanical polish, to sub-nanometre roughness. The surfaces are cleaned, activated with a plasma treatment, and brought into contact. The dielectrics fuse first through Van der Waals forces. A mild anneal at two hundred to four hundred degrees Celsius then causes the copper pads, now in intimate contact across the interface, to diffuse into each other and form a continuous copper interconnect.

No solder, no gap. The two dies behave as a single piece of silicon for signalling purposes. Pitches below ten microns for logic. Sony has demonstrated zero point seven microns for image sensors.

Hybrid bonding is the only way to drive pitch below the microbump floor. The operational catch: it is extremely unforgiving of surface contamination. A single particle ruins the bond. It requires near-fab-level cleanliness in the packaging step. This is part of why the line between fab and pack is blurring, which I'll come back to.

### Which bonding method at which rung

To summarise the bonding-to-rung mapping. Rung one and Rung two, flip-chip and fan-out, use mass reflow. Rung three, silicon bridge, can use either reflow or TCB. Rung four, silicon interposer, uses reflow for dies to interposer, TCB for HBM stacks on top. Rung five, three-D TSV stacking, requires TCB. And Rung six, hybrid bonding, is itself a bonding method, direct copper-to-copper.

Memorise that mapping. When you hear AMD's V-Cache uses SoIC, you now know, without anyone saying it, that the technology is hybrid bonding. When you hear HBM3 stacks are twelve-high, you know TCB is on the bill of materials.

## Part five. The vendor map

Here's where most writing on advanced packaging drowns the reader, by presenting brand names cold, without the underlying structure. Now we can walk through every significant brand name and you'll already know where it sits on the ladder.

### TSMC

TSMC's naming is logical once you see the structure. InFO is the fan-out family, Rung two. CoWoS is the interposer family, Rung four. SoIC is the hybrid bonding family, Rung six.

Within InFO. InFO-R is the baseline, used in Apple A-series and M-series chips. InFO-PoP is package-on-package, with DRAM stacked on top of the logic InFO package, Apple's approach before the M-series. InFO-oS, on substrate, places a fan-out on top of an organic substrate for larger or higher-I/O configurations. InFO-SoIS, System on Integrated Substrate, does heavy fan-out with up to fourteen RDL layers, for networking silicon. InFO-SOW, System on Wafer, is wafer-scale fan-out. Tesla Dojo D1 tile reportedly uses this. And InFO-LSI, Local Silicon Interconnect, is a fan-out with silicon bridges embedded for die-to-die links. Apple M1 Ultra's UltraFusion interconnect reportedly uses this. So InFO-LSI is a Rung two plus three hybrid.

Within CoWoS. CoWoS-S is the original and still the highest-volume. Passive silicon interposer, RDL patterned lithographically. Every major AI GPU with HBM. CoWoS-R is an RDL-first variant with an organic-based interposer component, cheaper but less dense. CoWoS-L is newer, using a mix of silicon bridges and fan-out-style RDL. Nvidia Blackwell uses this. It's functionally a Rung three plus four hybrid.

Within SoIC. Two flavours by flow. Chip-on-Wafer, CoW, mounts singulated dies on a wafer and bonds them. AMD's three-D V-Cache is CoW SoIC, at seventeen microns pitch. Wafer-on-Wafer, WoW, bonds two full wafers, then singulates afterwards. Graphcore's IPU Bow uses this.

### Intel

Intel's naming tracks architectural intent. EMIB is silicon bridge, Rung three. Foveros is TSV stacking, Rung five. Foveros Direct is hybrid bonding, Rung six. Co-EMIB combines the three-D and bridge techniques.

EMIB first deployed in twenty eighteen on Kaby Lake G. Sapphire Rapids uses EMIB extensively. Bridge line-and-space has gone from five microns down to two across generations. Pitch from fifty-five down to forty. Intel claims near-one-hundred-percent yield on these bridges, challenging ASE's eighty-to-ninety-percent marketing for the comparable FOEB.

Foveros first deployed in twenty twenty on Lakefield, at fifty microns pitch. Ponte Vecchio uses it with forty-seven chiplets combined with EMIB at thirty-six microns pitch. Meteor Lake uses a later Foveros generation for its compute, GPU, and I/O tiles.

Foveros Omni, also called ODI, Omni-Directional Interconnect, is a more flexible variant. It uses copper pillars in addition to or instead of microbumps, allowing the top die to have a larger footprint than the base die. Thirty-six microns pitch. Meteor Lake uses this too.

Foveros Direct is Intel's brand for hybrid bonding, positioned for future products.

Co-EMIB is a composite: multiple Foveros three-D stacks stitched together with EMIB. A Rung three plus five hybrid.

### Samsung, ASE, and Amkor

Samsung has FOSiP, Fan-Out System in Package, at Rung two. Tesla HW4.0 uses it. I-Cube is Samsung's silicon interposer, competing with CoWoS-S. Baidu's Kunlun AI accelerators use it. X-Cube is Samsung's hybrid bonding, positioned against SoIC.

ASE has FoCoS at Rung two. FOEB at Rung three, with a glass-carrier variant. AMD's MI200 and MI250X use it. SPIL, an ASE subsidiary, has NTI, a high-end Rung two with zero point five micron L-S on the first RDL layer.

Amkor has WLFO at Rung two. And SLIM, a high-end Rung two with zero point four micron L-S on the first layer.

### Sony and YMTC

Worth a separate mention because they were there first with hybrid bonding, before the logic industry caught up.

Sony has been shipping hybrid-bonded CMOS image sensors since twenty sixteen. They have two-stack, with pixel die over circuitry die. Three-stack: pixel, DRAM buffer, circuitry. And a forthcoming four-stack that separates the pixel transistor from the photodiode. Their pitches reach zero point seven microns, finer than anything in the logic world. Image sensors are where the industry learned that hybrid bonding works at scale.

YMTC, Yangtze Memory Technology, uses hybrid bonding wafer-to-wafer for NAND flash, in a process they call XStacking. The idea: fabricate the NAND array and the CMOS periphery, the control logic, on separate wafers optimised for each, then bond them. This gave YMTC a real density advantage over Samsung, Micron, SK Hynix, and Kioxia for a couple of generations. The equivalent product architectures at competitors are only now catching up.

## Part six. Why the lines are blurring

There's a view in the trade press that the conventional taxonomy, two-D, two-point-one-D, two-point-three-D, two-point-five-D, three-D, is dissolving as technologies muddle together. That's half right. The better framing: the category axis was always wrong. What's actually happening is that several technologies are converging on the same rung of the pitch ladder from different starting points.

Concretely. Fan-out with embedded silicon bridges, InFO-LSI, FOEB, reaches Rung three from the fan-out direction. EMIB reaches Rung three from the organic-substrate direction. Coreless ABF substrates with three-to-six micron line-and-space, Unimicron, Cisco's research, are reaching toward Rung three from the commodity-organic direction. And CoWoS-L combines silicon bridges with organic RDL to reach Rung three-to-four from the silicon-interposer direction.

Five different names, one functional sweet spot: somewhere between organic-only and silicon-interposer. Dense enough for die-to-die logic links, cheap enough not to need a full interposer. The point-one-D and point-three-D vocabulary tries to differentiate these by how they got there. The rung they got to is the same.

A modern AI package is often hybrid in exactly this way. AMD's MI300 is a working example. SoIC hybrid-bonded tiles at Rung six on top of logic-and-I/O dies entered with Rung five TSVs, sitting next to HBM stacks on a silicon interposer at Rung four, all on an ABF organic substrate at Rung one, on a PCB. Five rungs in one device. There is no one technology.

The hidden thesis. The real twenty-twenties story in advanced packaging is not that one technology won. It's that the cost curve for every rung has shifted downward, so that multi-rung packages have become economic. A twenty-fifteen-era AI accelerator could afford a silicon interposer only if the product was priced above ten thousand dollars, a Nvidia P100 or Google TPU. A twenty twenty-four AI accelerator can afford a silicon interposer plus hybrid-bonded SRAM plus TSV-stacked HBM in the same device. That's not a taxonomy shift. It's a cost-curve shift.

## Part seven. The product atlas

Here's where the famous products sit on the ladder.

Nvidia A100. CoWoS-S. Roughly eight hundred and twenty-six square millimetre logic die. Six HBM2e stacks. Reticle-stitched interposer.

Nvidia H100. CoWoS-S, with a larger reticle-stitched interposer. Eight hundred and fourteen square millimetre logic die. Five HBM3 stacks.

Nvidia Blackwell, B100 and B200. CoWoS-L. Two logic dies joined by silicon bridges. Eight HBM3e stacks. Plus RDL fan-out elsewhere.

AMD MI250X. ASE FOEB. Two GPU dies on a fan-out-with-silicon-bridge substrate. Plus HBM.

AMD MI300. TSMC CoWoS-S base, with SoIC hybrid-bonded logic tiles above an I/O die. A Rung four plus Rung six sandwich.

AMD's three-D V-Cache, in Zen 3 and later. TSMC SoIC CoW. Sixty-four megabytes of L3 SRAM cache bonded on top of a CCD at seventeen microns pitch.

Apple A15, A16, A17. TSMC InFO-R. Single SoC in a fan-out package.

Apple M1 Ultra and M2 Ultra. TSMC InFO with a silicon bridge joining two die halves. What Apple brands UltraFusion. That's InFO-LSI.

Tesla Dojo D1 training tile. TSMC InFO-SOW, wafer-scale fan-out. Twenty-five D1 dies on one reconstituted wafer.

Tesla HW4.0, the full-self-driving inference chip. Samsung FOSiP.

Google TPU v4. TSMC CoWoS-S.

Amazon Trainium and Graviton 3. CoWoS-S.

Intel Kaby Lake G, back in twenty eighteen. First shipping EMIB product.

Intel Lakefield. First Foveros, at fifty microns pitch.

Intel Ponte Vecchio. Forty-seven chiplets. EMIB plus Foveros at thirty-six microns pitch.

Intel Sapphire Rapids. Four tiles joined by EMIB at fifty-five microns pitch, alongside one-hundred-micron standard flip-chip for the rest of the connections. A mixed-pitch package.

Intel Meteor Lake and Arrow Lake. Foveros Omni with mixed-pitch interfaces. One hundred and thirty, one hundred, and thirty-six microns.

HBM3 modules from Samsung, SK Hynix, and Micron. Rung five TCB stacking. Twelve dies of thirty-micron thickness.

Sony stacked CMOS image sensors. Rung six hybrid bond at zero point seven microns pitch.

YMTC NAND. Rung six XStacking, wafer-to-wafer bonding.

There's a detailed anatomy diagram in the written version showing the canonical AI accelerator package, a CoWoS-S setup with HBM. From the bottom up: PCB, BGA balls, ABF organic substrate, C4 bumps, silicon interposer, reticle-stitched, with TSVs through it, microbumps, then a logic die flanked by HBM stacks, topped with a thermal interface material and a lid. The interposer is what makes it Rung four. The HBM stacks themselves are Rung five. A single AI GPU package runs three different tiers of interconnect density in parallel.

Once you can read that atlas, CoWoS-L with HBM3e and NVLink-C2C decodes to Rung three plus four with silicon bridges and organic RDL, carrying an HBM Rung five stack, with high-speed serial links between packages. The trade press becomes readable. That's the whole goal.

## Closing thought

The instinct that the categories are dissolving is correct. What usually goes unsaid is why. The category names were always surface marketing. The underlying physics has one axis, interconnect density, measured in pitch. And one secondary axis, dimensionality. Every product is a point in that two-D space, and every vendor sells multiple products across multiple quadrants of it.

If you remember one thing from this, make it the ladder. If you remember two, add the bonding-method cross-product. If you remember three, add the substrate material choice, organic, silicon, glass, that sits inside each rung. Everything else, brand names, two-point-one-D versus two-point-three-D, which vendor's RDL-first process yields three percent better, is detail on that frame.

The next decade of this industry will be about pushing every rung's cost curve down further, so multi-rung packages become standard in lower-margin products. Expect hybrid bonding to appear in laptops. Expect silicon bridges in consumer GPUs. Expect the vocabulary to keep multiplying. But the ladder won't change. Only the price tags on each rung will.

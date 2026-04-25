# Memory Cells: RemNote Flashcards

## The problem flash solves

- What hole in the memory market did flash fill? <> Non-volatile, electrically rewriteable, dense enough to be cheap — D-RAM was volatile, S-RAM was expensive, R-O-M was write-once
- D-RAM stores each bit as {{charge on a tiny capacitor}} that leaks within {{milliseconds}} and must be refreshed
- S-RAM stores each bit in a {{flip-flop made of six transistors}}, which is fast but {{expensive}}

## Floating gate invention

- Who invented the floating gate, where, and when? <> Dawon Kahng and Simon Sze at Bell Labs in {{1967}}
- What is a floating gate? <> A second gate inserted between the control gate and channel of a transistor, made of {{polysilicon}} and completely surrounded by {{silicon dioxide insulator}} so it connects to nothing
- How is a floating-gate bit read? <> Apply a moderate voltage to the control gate; if trapped electrons are present they {{shift the threshold voltage higher}} and the transistor will not conduct
- What two physical mechanisms are used to write a floating-gate cell? <> {{Hot-electron injection}} and {{Fowler-Nordheim tunnelling}}
- What wears out across program-erase cycles, limiting endurance? <> The {{tunnel oxide}} — repeated high-field stress eventually causes breakdown
- "Electrons in a bucket" — what is the bucket made of and what are the walls? <> Bucket is {{polysilicon}}, walls are {{silicon dioxide}}

## EPROM, EEPROM, flash

- Who built the first EPROM and when? <> {{Dov Frohman at Intel}} in {{1971}}
- How were EPROMs erased? <> {{Ultraviolet light}} through a {{quartz window}} on the chip package — UV photons knock electrons off the floating gate
- Who invented EEPROM and when? <> {{George Perlegos at Intel}} in {{1978}}
- Why was EEPROM expensive? <> Each cell needed {{extra transistors for byte-level erase}}, killing density
- Who invented flash memory and where? <> {{Fujio Masuoka at Toshiba}} in {{1980}}
- What is the key trade-off that defines flash vs EEPROM? <> Flash erases in {{large blocks}} instead of {{single bytes}}, sacrificing fine-grained writability for {{much higher density}}
- Why is it called "flash"? <> Erasing a whole block reminded Masuoka of a {{camera flash}}
- What did Masuoka receive from Toshiba for inventing flash? <> A small bonus — he later sued and got around {{$800,000}} for an invention that built a {{>$500B annual industry}}

## NAND vs NOR

- NOR flash wires its cells in {{parallel}}, like a {{NOR gate}}
- NAND flash wires its cells in {{series strings}}, like a {{NAND gate}}
- What is NOR flash optimised for? <> {{Random read speed}} and {{execute-in-place (XIP)}} of code — used for BIOS and embedded firmware
- What is NAND flash optimised for? <> {{Density and cost}} — used for mass storage (USB, S-D, SSDs)
- Who shipped commercial NOR flash first and when? <> {{Intel}} in {{1988}}
- Who shipped commercial NAND flash first and when? <> {{Toshiba}} in {{1989}}
- Roughly how does NAND outsell NOR by bit volume? <> Roughly {{100 to 1}}

## Bits per cell ladder

- SLC stands for {{Single-Level Cell}}, stores {{1}} bit, has {{2}} states, ~{{100,000}} P/E cycles
- MLC stands for {{Multi-Level Cell}}, stores {{2}} bits, has {{4}} states, ~{{10,000}} P/E cycles
- TLC stands for {{Triple-Level Cell}}, stores {{3}} bits, has {{8}} states, ~{{3,000}} P/E cycles
- QLC stands for {{Quad-Level Cell}}, stores {{4}} bits, has {{16}} states, ~{{1,000}} P/E cycles
- PLC stands for {{Penta-Level Cell}}, stores {{5}} bits, has {{32}} states, <{{500}} P/E cycles — mostly research
- Why does each extra bit per cell hurt endurance and speed? <> Each extra bit {{doubles the number of voltage levels}} you must distinguish; the windows shrink, requiring more aggressive {{ECC}} and slower {{multi-pass programming}}
- The deep insight on bits per cell: NAND has been getting denser not just by shrinking cells but by raising {{information density per cell}} — the same bucket now holds 4-5 bits instead of 1

## Why planar NAND hit a wall (~2013-2015)

- What four physical problems killed planar NAND scaling? <> {{Electron count too low for reliable multi-bit reads}}, {{cell-to-cell capacitive interference}}, {{tunnel oxide wear}}, {{lithography cost without EUV}}
- Roughly how many electrons does a 15nm planar floating gate hold? <> Around {{100}} electrons total — quantum noise becomes catastrophic at QLC voltages
- What is "neighbour coupling" in planar NAND? <> Adjacent {{floating gates couple capacitively}}, so programming one cell shifts the apparent state of its neighbours

## Charge trap flash

- What does CTF stand for? <> {{Charge Trap Flash}}
- What older structure is CTF based on? <> {{SONOS}} — Silicon-Oxide-Nitride-Oxide-Silicon, known since the 1970s
- What replaces the conducting polysilicon island in CTF? <> A non-conducting {{silicon nitride layer}} where electrons sit in {{discrete trap sites}}
- Why is CTF more defect-tolerant than floating gate? <> A pinhole in the tunnel oxide drains the entire {{conducting floating gate}}, but only the electrons {{near the defect}} leak from a charge-trap nitride layer
- Why was CTF a prerequisite for 3D NAND? <> {{Floating-gate polysilicon}} cannot be reliably deposited as discrete islands down a {{high-aspect-ratio memory hole}}; silicon nitride deposits {{conformally}} along the whole hole

## 3D NAND architecture

- Who shipped the first commercial 3D NAND and when? <> {{Samsung}} V-NAND in {{2013}}
- Who originally published the 3D NAND concept and what was it called? <> {{Toshiba}} in {{2007}}, called {{BiCS}} (Bit Cost Scalable)
- What is the core idea of 3D NAND? <> Rotate the cells {{90 degrees}} and stack them {{vertically}} — get density from layer count instead of feature size
- What process node is typical for 3D NAND? <> Around {{30-40nm}} — much more relaxed than the planar NAND it replaced
- What are "memory holes"? <> Vertical holes drilled through the entire stack of alternating conductor/insulator layers, ~{{80-100nm wide}}, thousands of nm deep
- What layers line a 3D NAND memory hole, from outside in? <> {{Blocking oxide}} → {{silicon nitride charge trap layer}} → {{tunnel oxide}} → {{polysilicon channel}}
- In 3D NAND, what is each conductor layer in the stack? <> A {{word line}} — a horizontal control gate that wraps around every memory hole passing through it

## Where the technology stands (2026)

- Roughly how many layers do leading 3D NAND products have today? <> Over {{200}}, with roadmaps to {{500+}} by end of decade
- What is "string stacking" or "deck architecture"? <> Above ~96 layers, etching one continuous hole becomes impossible — manufacturers etch {{~96 layers, deposit a tier, then etch another ~96 on top}}, aligning the two
- What does CuA stand for in 3D NAND? <> {{CMOS-under-Array}} — peripheral logic built {{directly underneath}} the memory stack
- What does CBA stand for? <> {{CMOS-Bonded-Array}} — peripheral logic built on a {{separate wafer}} and {{hybrid-bonded}} onto the memory wafer
- Who are the four global NAND players? <> {{Samsung}}, {{SK Hynix (with Solidigm)}}, {{Micron}}, and {{Kioxia (with Western Digital)}}

## Emerging memories

- What does PCM stand for and what is its mechanism? <> {{Phase Change Memory}} — stores bits as {{crystalline vs amorphous phases}} of a {{germanium-antimony-tellurium}} chalcogenide alloy
- What was Intel's PCM-derived product and when was it killed? <> {{Optane (3D XPoint)}}, killed in {{2022}} — could not beat D-RAM on price or NAND on density
- What does MRAM stand for and what is the current variant? <> {{Magnetic RAM}}; current variant is {{Spin-Transfer Torque MRAM (STT-MRAM)}}
- What niche is MRAM actually winning today? <> {{Embedded memory in microcontrollers}}, replacing eFlash that fabs cannot manufacture below ~22nm
- What does ReRAM stand for and what is its mechanism? <> {{Resistive RAM}} — forms and breaks {{conductive filaments}} inside a {{metal-oxide layer}}
- What is the consistent failure mode of emerging memories? <> Each is excellent on {{one or two axes (speed, endurance, retention)}} but {{loses on cost}} — NAND's 30-year manufacturing learning curve is the moat

## Investment-relevant takeaways

- 3D NAND scaling is primarily a {{capital equipment story}}, not a {{lithography story}} — the hard parts are {{etch and deposition}}
- Which equipment vendors win from 3D NAND scaling? <> {{Lam Research}}, {{Applied Materials}}, and {{Tokyo Electron}}
- D-RAM is hitting the {{EUV lithography}} wall now, unlike NAND
- What is HBM and who leads it? <> {{High-Bandwidth Memory}} — stacked D-RAM dies on a logic base die, used in AI accelerators; {{SK Hynix}} leads, Samsung catching up, Micron third
- The two technical metrics worth tracking in memory: <> {{NAND layer count}} and {{HBM stack height/bandwidth}}

## One-line summary card

- Summarise the entire arc of memory cell evolution: <> Started with a leaky bucket of electrons surrounded by glass; made the bucket smaller until it stopped working; changed the bucket from a metal island to an insulator layer so a single defect could no longer drain it; stopped shrinking and started stacking, hundreds of layers deep; and along the way learned to read not just whether the bucket was full but how full it was, to four bits of precision.

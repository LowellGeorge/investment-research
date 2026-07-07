# The Four Bottlenecks of AI Compute

## Bottleneck One: Advanced Foundry and Packaging Capacity

Almost all AI compute is manufactured by TSMC, the Taiwan Semiconductor Manufacturing Company, because TSMC has the advanced processes needed, in the volume needed, and with the advanced packaging required to integrate multiple chiplets on interposers and substrates. It is an almost-monopoly for data center AI. TSMC's revenues are expected to grow four times from 2023 to 2028. Unlike the memory companies, it has not radically raised prices, though its margins are trending upward into the mid sixty percent range.

Recently TSMC raised its outlook for the global semiconductor market to 1.5 trillion dollars by 2030, up from its earlier estimate of 1 trillion dollars, according to Reuters. AI is expected to be fifty-five percent of the total market, followed by twenty percent for smartphones and ten percent for automotive.

TSMC's CEO, CC Wei, says, "it will be a long time before we can meet customer demand," according to Bloomberg. This is despite TSMC investing heavily in multiple new fabs and packaging facilities in the USA and in Taiwan. Its CoWoS packaging capacity — that is, Chip-on-Wafer-on-Substrate — is essential for AI compute, and is growing at an eighty percent compound annual growth rate from 2022 to 2027. TSMC is outsourcing some CoWoS packaging to ASE and Amkor to help with demand. AI accelerator wafer demand is growing more than eleven times in the same period.

TSMC is developing CoPoS packaging — Chip-on-Panel-on-Substrate — to replace CoWoS, using glass core substrates to cut costs and boost wafer utilizations.

TSMC has done an amazing job of developing advanced processes and packages while ramping numerous manufacturing plants in multiple locations worldwide. But even TSMC can only grow so fast — people are the ultimate limiter.

TSMC is expected to prioritize Nvidia, AMD, Broadcom, and its other major strategic customers. TSMC spends a lot of effort to carefully evaluate its customers' wafer demands against all the market data they can find, to validate that orders are realistic. The foundry is also careful to take care of smaller companies it sees as having high potential.

There are few good alternatives to TSMC.

Intel and Samsung have leading-edge process nodes, but with much less capacity and less developed packaging capabilities and capacities.

SMIC, the Semiconductor Manufacturing International Corporation, in China, lags TSMC, partly because US export controls block access to advanced lithography. Despite this, SMIC is able to build trailing-edge processes — much less power efficient, but not a concern in China where electricity is abundant — that Huawei uses to build performance-competitive AI compute.

GlobalFoundries abandoned its finFET development years ago. Its most advanced node is twelve nanometers, which is not useful for data center AI.

Given the huge demand, it seems likely that major players with deep pockets will try building chips with Intel and Samsung — perhaps their lower volume or lower complexity products, especially if that frees up their TSMC allocations for products that cannot be outsourced. Rumors are that Google has given Intel, or perhaps Samsung, orders for millions of TPUs, or Tensor Processing Units. President Trump recently said Apple will use Intel, though Apple has not confirmed this. It seems likely that one of, or perhaps both, Intel and Samsung may emerge as a viable number two to TSMC, but it will be a long road.

All foundries, except SMIC, are bottlenecked by the Netherlands' ASML, Advanced Semiconductor Materials Lithography, which is the only supplier of advanced lithography manufacturing equipment. It does not seem to be the bottleneck in capacity expansion, though.

All foundries are also bottlenecked by ABF, Ajinomoto Build-up Film, which is used to connect GPU dies to HBM stacks. Japan's Ajinomoto makes more than ninety-five percent of the global supply of ABF. It raised prices thirty percent in 2026, and projects a supply gap of more than twenty percent in 2027, according to the Wall Street Journal.

## Bottleneck Two: Memory — DRAM and Flash Capacity

In the 1990s there were dozens of manufacturers of DRAM. Today, three companies dominate — SK hynix, Samsung, and Micron.

There is a rising DRAM supplier in China, CXMT, with revenues of 8 billion dollars in 2025. Its sales are primarily in China and its products lag those of the industry leaders in specs. Yangtze Memory is close behind, building three new factories in China to double its current capacity, according to the Wall Street Journal.

The critical shortage is in HBM, high-bandwidth memory DRAM, which is critical for all GPUs and XPUs made by Nvidia, AMD, Google and Amazon. About eighty percent is made in South Korea.

Manufacturing more HBM requires DRAM wafer fab capacity, but also complex packaging capacity. HBM is comprised of eight-, twelve-, or sixteen-high DRAM stacks, with through-vias to ever-more memory in a small space. This is very challenging to manufacture.

DRAM has traditionally been a brutal boom and bust business — high prices and margins during shortages, then years of oversupply, low prices and losses. This makes DRAM companies very conservative to add capacity. They worry they will swing back into oversupply. DRAMs are very, very complex, so a new DRAM process takes more than five years to develop, and a fab several years.

Unlike TSMC, DRAM companies are raising prices to meet demand. They are working on strategic supply agreements, such as the one recently announced between Micron and Anthropic, to lock in customer demand for the long term, typically with upfront cash. As a result, all three companies are now more than 1 trillion dollars in market cap.

JEDEC recently approved a new version of HBM that uses more standard packages and glass substrates that can avoid the ABF shortage. This will take years to phase in.

## Bottleneck Three: Data Centers, Especially Power

The biggest problem for data centers is power. Amazon's CEO named this as the number one constraint, according to the Wall Street Journal.

Data centers are using whatever power they can get, wherever they can get it — grid power, natural gas, Bloom Energy fuel cells, Babcock and Wilcox steam turbines, solar plus batteries, and more.

The grid cannot add capacity fast enough for the demand, and there is growing community resistance in many locations to data centers increasing their local electricity prices.

Three companies — Tesla, Sunrun, and Renew Home, a Google spin-off — recently announced they were working together to free up enough electrical capacity to meet the needs of seventeen large data centers during periods of high demand. They will do this by getting consumers to opt in and let them tap their home batteries during periods of high demand.

Hyperscalers are contracting natural gas at the production point where supply exceeds what pipelines can take to markets. Chevron recently struck a twenty-year agreement to sell electricity to Microsoft, working with Joulent, which is building a 2.7 gigawatt power generation plant on a campus in the heart of the Permian Basin oil-and-gas field in West Texas, according to the Wall Street Journal.

It is not just the power sources in short supply. All the other items needed to power a data center are in short supply — the transformers, high-voltage breakers, and so on. GE Vernova, the leading gas turbine supplier, is sold out through 2029.

Solar and batteries are components of an off-grid power solution, but they are not economic as a solution by themselves, because the worst-case scenario is a winter cloudy day without enough solar to charge the batteries for the long winter night. The capital required is multiples of what is required for solar on a sunny summer day with a short summer night. So solar and batteries will be used in combination with natural gas, especially if natural gas or the turbines are in short supply.

There is also growing resistance in many communities and states to data centers. Even in Texas, the Texas Tribune recently reported most Texans oppose data center construction. The biggest concerns are that data centers will drive up electricity prices and use up scarce water. Cerebras' CEO, Andrew Feldman, says that the California almond industry uses more water than all the data centers in the USA, according to CNBC.

## Bottleneck Four: Lasers for Optical Interconnect

This is perhaps the least daunting bottleneck, because the bottleneck is not here yet.

Lasers are used in scale-out pluggable transceiver optical links between all the top-of-rack switches in the data center.

Lasers will also be used in scale-up co-packaged optics links, that will become prevalent over the next two to five years. There are ten to a hundred times more scale-up links than scale-out.

The largest three laser suppliers are Coherent, Lumentum, and Sumitomo, which together have sixty-eight percent share. They have their own manufacturing facilities in multiple locations. Lumentum is the largest supplier. Coherent is the first to move to six-inch wafers for indium phosphide. There are many other suppliers, including Broadcom, Mitsubishi, MACOM, Applied Opto, and Landmark.

AI laser leaders Lumentum and Coherent are now over 60 billion dollars market cap each, ten times what they were just a year ago. Both are sold out. Both require up-front cash to get capacity. In March, Nvidia announced a 2 billion dollar investment in each of them to secure supply chain capacity. This happened shortly before Nvidia's GTC, where Jensen Huang showed co-packaged optics starting on the Nvidia roadmap from 2028.

At its briefing at the Optical Fiber Conference in March, Lumentum showed it is rapidly growing indium phosphide capacity, but demand is growing even faster.

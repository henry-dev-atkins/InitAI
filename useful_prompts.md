# Useful Prompts

## Software Complete
I think we can complete the software requirements without extra big runs (simple quick tests <1min each, except data downloads where relevant) because we have the spec and context. 
We just need to add a handful of classes, functions, and configs which are quick to validate that they will work. 
We are not running the big-stuff (real runs, anything lasting >1min) and are ONLY doing code edits. 
Please plan this work and ORCHESTRATE your coding team to complete the software work that is needed, such that when I next open this repo with available hardware, I just just hit execute and it will run everything for my paper.


## CAT SPEC COMPLETION: 6d-5h-8m
Perfect result from a SPEC_REVIEW and fast runtimes (<1.5hr for the quick test simulation of the paper suite). Please ensure you do not get caught up chasing software BS - focus on spec requried capabilities. Minimal software wrappers, parsers, and oterh software BS. This means that no special logic surrounds quick test suite except that the runs have fewer steps - everything else must be identical. Specifically, we are making a research suite of high effort and quality, to be published in the most prestigious journal. We work at multiple layers, high level entry API's, all the way down to low level cpp kernels - you do it all and do not shy away from any work no matter how much effort it requires.This PC have limited memory so please minimise run count, and use [SESSION.CLEAN] to move old/ incremental/test/PoC runs to `archive/`.When choosing solutions, pick the 'real fix' not just reporting. Never ever make 'special case' edits for branches within the repo, unless a high level requirement needs it. We may have logic and implementations NOT described/required by the SPEC, these need removing as we do not support legacy work. You are [ORCHESTRATOR] and cannot code yourself, and at each turn ask yourself: 
1) Is this software BS which we want to avoid? 
2) Am I going in circles, which we want to avoid and fix with DIAGNOSE runs? 
3) Should I pass this to an agent, so work can be conducted in parallel?
4) Am I just 'replacing' old logic, instead of furthering the resarch goal?
class PromptGenerator:
    prompt_type = 0
    
    def __init__(self, prompt_type):
        self.prompt_type = prompt_type
        
    def generate_prompt(self, issue):
        if self.prompt_type == 1:
            return self._generate_prompt1(issue)
        elif self.prompt_type == 2:
            return self._generate_prompt2(issue)
        elif self.prompt_type == 3:
            return self._generate_prompt3(issue)
        elif self.prompt_type == 4:
            return self._generate_prompt4(issue)
        else:
            raise ValueError("Invalid prompt type")

    def _generate_prompt1(self, issue):
        return f"""Does the issue below should have a "Self Admitted Technical Debt" label? Your answer should be "YES" or "NO".
issue text{{
    {issue}
}}
        """

    def _generate_prompt2(self, issue):
        return f"""Does the issue below should have a "Self Admitted Technical Debt" label? Think step-by-step. YOUR ANSWER SHOULD START WITH "YES" OR "NO".
issue text{{
    {issue}
}}
"""

    def _generate_prompt3(self, issue):
        return f""" You are going to be identifying Self-Admitted Technical Debt through issues. 
Examples:
SATD Issue text{{
    "I wrote up the polling solution really quickly when I was late for work and never went back to fix it. Instead of saving message IDs or keeping track of the text of the poll as one variable, it saves a new copy of the poll every time someone adds or removes a vote. This is horrible and I'm embarrassed that I haven't fixed it yet"
}}
Answer: YES

Non-SATD Issue text{{
   "### Search before asking

- [X] I have searched the YOLOv5 [issues](https://github.com/ultralytics/yolov5/issues) and [discussions](https://github.com/ultralytics/yolov5/discussions) and found no similar questions.


### Question

Why is it set like this?
    hyp['box'] *= 3 / nl  # scale to layers
    hyp['cls'] *= nc / 80 * 3 / nl  # scale to classes and layers
    hyp['obj'] *= (imgsz / 640) ** 2 * 3 / nl  # scale to image size and layers
default  hyp['box'] : hyp['cls'] :  hyp['obj'] = 1:1:1
if my data nc is 3, hyp['box'] : hyp['cls'] :  hyp['obj'] = 1: 3/80 :1????

### Additional

_No response_"
}}
Answer: NO

SATD issue text{{
    "Logic for manipulating resource path (and paths generally, for that matter) is scattered and duplicated all over the application. This needs to be tracked and unified into a set of standard general-purpose path utilities."
}}
Answer: YES

Non-SATD issue text{{
    "title": "Add way to auto-update players' timezones"
    "body": "There's often confusion whenever daylight savings changes, because people forget to change their timezone on the website.
We can detect when the browser's timezone is different from the timezone on the player's profile. In that case, we can prompt the user if they want to change their profile timezone."
}}
Awnser: NO

Does the issue below should have a "Self Admitted Technical Debt" label? YOUR ANSWER SHOULD BE JUST "YES" OR "NO".
issue text{{
    {issue}
}}
"""

    def _generate_prompt4(self, issue):
        return f"""Analyze the given issue description to identify the presence of Self-admitted technical debt (SATD). Follow these steps to determine if SATD is present:

Step 1: Identify any mentions of shortcuts, workarounds, or temporary solutions in the issue description. These may indicate the presence of SATD.

Step 2: Look for phrases that suggest the implementation is incomplete, suboptimal, or requires future refactoring. Examples include "typo", "leak", "flaky", "unnecessary", "performance", "checkstyle", "spelling", "unused", "cleanup", "coverage", "TODO", "FIXME", "hack", "not ideal", "needs improvement" or similar expressions.

Step 3: Check if the issue description acknowledges any design or architectural limitations that may incur technical debt in the future.

Step 4: Determine if the issue description mentions any time constraints, pressure to deliver, prioritization of speed over quality or if the issue description discusses any compromises made in the implementation, such as using a less efficient algorithm, hardcoding values, or skipping necessary validations, which may lead to SATD.

Step 5: Consider if the issue description indicates any planned or required refactoring, code cleanup, or performance optimizations in the future.

Based on the presence or absence of the above indicators, conclude whether the issue contains Self-admitted technical debt or not. Provide a detailed analysis of each identified instance of SATD, including the relevant excerpt from the issue, an explanation of why it is considered SATD, and any additional context or insights.

Start your answer with "YES" or "NO".

issue text{{
    {issue}
}}
        """
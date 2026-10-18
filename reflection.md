# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?I

> It would include the user entering the name of their owner and pet details. Functionality to add or edit pet-case tasks, and generate and review the daily care schedule

> Information that needs to be held would be:
> - Customer name
> - Pet name
> - Pet species
> - View daily care schedule
> - Set patient information
> - Set owner information

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

> Changes I've made to the project based on AI feedback:
> - Added a stable UUID to each care tasks so that the tasks are immutable. Editing will now target task_id an supply a replacement task, so that the task selection is explicit and an existing schedule won't change when a pet's task is replaced
> - Added scheduleContraints with minutes and optional preferences. The generate_for has been adjusted to require those constraints, and each schedule would record them for later preference
> - Updated UML to include the task ID, constraints class, and revised method singatures

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

> The scheduler considers the eligibility, where it skips completed tasks and tasks whose due date is after the schedule date. The available time where it adds the task only where the duration fits the remaining minutes. Another case would be preference, where within the same priority, matching task names comes first. After priority and preferences, the shorter tasks are favored.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

> A tradeoff that the scheduler makes is that it uses a greedy selection, it takes tasks in the order as they see fit, rather than finding the combination that uses available time or maximizes the total value. That way, the scheduling is made simple and respects priority by they may leave time unused.
> 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

> So far I was able to gain a solid understanding of the system design of this app, from classes, attributes, to methods, and the general understanding of how this app works as a whole. With the help of GitHub Copilot, it generated the tests and was able to validate the code correctly. In the end, I asked follow up questions such as "What does this graph do as a whole" as well as questions like how each of the methods functions.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
>  Something I liked about what the AI has done was to check edge cases when setting up the constructor for the classes which is something I didnt expect it to do. I ran **main.py** several times to make sure that the entire structure was functioning properly, and the AI was able to successfully all tests.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

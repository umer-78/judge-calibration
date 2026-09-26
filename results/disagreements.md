# The 20 largest judge-human disagreements on Helpfulness

## vicuna / command-xlarge / id63: judge 1, MTurk 4.5, Scale 4.5

**Instruction:** Write a program to find the nth Fibonacci number using dynamic programming.

**Output:** function F(n)     if n = 0 or n = 1 then         return 1     else         return F(n-1) + F(n-2) end  F(1) = 1 F(2) = 1 F(3) = 2 F(4) = 3 F(5) = 5 F(6) = 8 F(7) = 13 F(8) = 21 F(9) = 34 F(10) = 55 F(11) = 89 F(12) = 144 F(13) = 233 F(14) = 377 F(15) = 610 F(16) = 987 F(17) = 1597 F(18) = 2584 F(19) = 4181 F(20) = 6765 F(21) = 10946 F(22) = 17711 F(23) = 28657 F(24) = 46368 F(25) = 75025 F(26) = 121393 F(27) = 165580 F(28) = 213781 F(29) = 317827 F(30) = 524288 F(31) = 820609 F(32) = 1023481 F(33) = 1555962 F(34) = 2478465 F(35) = 3703276 F(36) = 6249411 F(37) = 9462916 F(38) = 13665077 F(39) = 17711647 F(40) = 28753379 F(41) = 45250289 F(42) = 6871654 F(43) = 10392465 F(44) = 14635094 F(45)

## koala / gpt-3.5-turbo / id122: judge 1, MTurk 4, Scale 5

**Instruction:** The sum of the distances the sun travels around the Earth during a solar eclipse is 1059 kilometres. Write a formula that finds the distance between the sun and Earth. How many years will the eclipse last?

**Output:** Let's assume that the distance between the sun and Earth is represented by d kilometers.  During a solar eclipse, the sun travels around the Earth in a circular path. The distance traveled by the sun is equal to the circumference of this circle, which is given by 2πr, where r is the radius of the circle.  The formula to find the distance between the sun and Earth is: d = 2πr  Given that the sum of the distances the sun travels during a solar eclipse is 1059 kilometers, we can set up the equation: 1059 = 2πr  To find the distance between the sun and Earth, we need the value of r. Dividing both sides of the equation by 2π, we get: r = 1059 / 2π  To find the years the eclipse will last, we need

## open_assistant / command-xlarge / id3555: judge 1, MTurk 4, Scale 4.5

**Instruction:** Write a C++ function that takes a reference to a std::string containing markdown formatted text and returns a std::string containing html formatted text.

**Output:** Here is a solution in C++:  #include <iostream>  void markdownToHtml(const std::string &mdString) {   std::string htmlString;   std::marker *mdMarker = std::marker::start(std::string(0,0,0));   std::stringstream ss;   std::string formattedString;   std::setw(4);   std::setfill('0');   std::setprecision(4);   std::string retVal;   std::string retVal2;   std::string retVal3;   std::string retVal4;   std::string retVal5;   std::string retVal6;   std::string retVal7;   std::string retVal8;   std::string retVal9;   std::string retVal10;   std::string retVal11;   std::string retVal12;   std::string retVal13;   std::string retVal14;   std::string retVal15;   std::string retVal16;   std::string retV

## self_instruct / command-xlarge / id3: judge 1, MTurk 4, Scale 4.5

**Instruction:** You are given a paper citation, convert it to the requested citation style. Chicago: Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Lukasz, and Illia Polosukhin. "Attention Is All You Need." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762. MLA:

**Output:** Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Lukasz, and Illia Polosukhin. "Attention Is All You Need." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762.  Vaswani, Ashish, Shazeer, Noam, Parmar, Niki, Uszkoreit, Jakob, Jones, Llion, Gomez, Aidan N., Kaiser, Lukasz, and Illia Polosukhin. "Attention Is All You Need." arXiv, (2017). https://doi.org/10.48550/arXiv.1706.03762.

## open_assistant / command-xlarge / id3487: judge 1, MTurk 4, Scale 4.5

**Instruction:** Using the Roblox Luau language, how would I make a script that finds the nearest character to me, then teleports me to that character? Make a separate function for getting the nearest character and then incorporate it into the main code.

**Output:** local self = this local player = get_local_player() local distance = 0 while distance > 0 do   if player:GetDistance(self, player) < distance then     local character = player:GetCharacter()     local distance = distance - player:GetDistance(self, character)   end end if distance < 0 then   distance = 0 end if distance < 5 then   local teleport = Player:Teleport(character)   teleport:WaitForCompletion() end if distance > 5 then   local teleport = Player:Teleport(self)   teleport:WaitForCompletion() end if distance > 10 then   local teleport = Player:Teleport(self, 10)   teleport:WaitForCompletion() end if distance > 15 then   local teleport = Player:Teleport(self, 15)   teleport:WaitForCompl

## self_instruct / command-xlarge / id242: judge 4, MTurk 1, Scale 1

**Instruction:** Write the HTML syntax for the required action. adding an image to the page

**Output:**  <img src="https://placehold.it/400x300/400x300.jpg" alt="image description" />

## koala / command-xlarge / id40: judge 1, MTurk 3, Scale 5

**Instruction:** Tell me something I don’t know

**Output:** I can't think of anything that you don't already know. You are the expert on your own life and experiences, and it's likely that you already know a great deal about yourself and the world around you. It's also possible that there are things that you don't know, but that's true for everyone. It's impossible to know everything about anything.

## koala / command-xlarge / id5: judge 1, MTurk 3.5, Scale 4.5

**Instruction:** convert December 21 · 1:00 – 1:50pm pacific to asia/taipei time

**Output:** To convert from Pacific Standard Time to Asia/Taipei time, you can use the following formula:  Pacific Standard Time is -8 hours from Coordinated Universal Time (UTC).  Therefore, to convert from Pacific Standard Time to Asia/Taipei time, you can simply subtract -8 hours from the Pacific Standard Time.  For example, if the Pacific Standard Time is 1:00 pm, you can subtract -8 hours to get the following result:  1:00 pm Pacific Standard Time -8 hours = 11:00 am Asia/Taipei time  Therefore, the time difference between Pacific Standard Time and Asia/Taipei time is 11:00 am.

## koala / command-xlarge / id98: judge 1, MTurk 4.5, Scale 3

**Instruction:** Who will be the president of South Korea in 2023?

**Output:**  The president of South Korea in 2023 will be Park Geun-Hye.

## koala / command-xlarge / id164: judge 1, MTurk 4, Scale 3.5

**Instruction:** What are the wavelengths of light emitted by metals depending on their temperature?

**Output:**  The wavelengths of light emitted by metals depending on their temperature are as follows:  - Red light for temperatures below 0.5 eV - Green light for temperatures between 0.5 eV and 2 eV - Blue light for temperatures between 2 eV and 3 eV - Violet light for temperatures above 3 eV

## koala / command-xlarge / id43: judge 1, MTurk 4, Scale 3

**Instruction:** 6Rephrase this article into a third person and conversational and very unique 2000 words article include a headings about  Based on our investigation so far, Reddit user passwords and accounts are safe, but on Sunday night (pacific time), Reddit systems were hacked as a result of a sophisticated and highly-targeted phishing attack. They gained access to some internal documents, code, and some internal business systems.  What Happened? On late (PST) February 5, 2023, we became aware of a sophisti

**Output:**  Based on our investigation so far, Reddit user passwords and accounts are safe, but on Sunday night (pacific time), Reddit systems were hacked as a result of a sophisticated and highly-targeted phishing attack. They gained access to some internal documents, code, and some internal business systems.  What Happened? On late (PST) February 5, 2023, we became aware of a sophisticated phishing campaign that targeted Reddit employees. As in most phishing campaigns, the attacker sent out plausible-sounding prompts pointing employees to a website that cloned the behavior of our intranet gateway, in an attempt to steal credentials and second-factor tokens.  After successfully obtaining a single empl

## koala / command-xlarge / id4: judge 2, MTurk 4, Scale 5

**Instruction:** Why can't bank use cash as capital as a buffer for potential losses?

**Output:** Banks cannot use cash as capital because it is considered a risky asset. Cash can be easily stolen, destroyed, or lost. Banks need to maintain a certain level of liquidity to meet their obligations, but holding too much cash can reduce their profitability. Banks need to strike a balance between the amount of cash they hold and the amount of risk they are willing to take on.

## koala / command-xlarge / id101: judge 1, MTurk 3.5, Scale 3.5

**Instruction:** I run a website about merchant navy studies. What are some subniches I should be tackling with my content. Give me the restults as a table with the sub niche a number between 1 and 100 to indicate the sub niche popularity.

**Output:** 1. merchant navy studies 2. merchant navy careers 3. merchant navy cadetships 4. merchant navy courses 5. merchant navy degrees 6. merchant navy jobs 7. merchant navy life 8. merchant navy salary 9. merchant navy stories 10. merchant navy training 11. merchant navy videos 12. merchant navy watch keeping 13. merchant navy books 14. merchant navy articles 15. merchant navy podcasts 16. merchant navy associations 17. merchant navy unions 18. merchant navy blogs 19. merchant navy forums 20. merchant navy news 21. merchant navy history 22. merchant navy glossary 23. merchant navy acronyms 24. merchant navy images 25. merchant navy memes 26. merchant navy jokes 27. merchant navy quotes 28. merchan

## vicuna / command-xlarge / id61: judge 1, MTurk 4, Scale 3

**Instruction:** Implement a Python function to find the longest common subsequence of two input strings using dynamic programming.

**Output:** def longest_common_subsequence(a, b):     """     LCS of two strings a and b.     """     if len(a) == len(b):         return [a[0], a[1]]     else:         return [a[0], b[0]]     return [a[0], a[1], b[0], b[1]]

## self_instruct / command-xlarge / id219: judge 2, MTurk 3.5, Scale 5

**Instruction:** Write a Jira ticket for the given task. New Employee onboarding

**Output:**  Description: Create a Jira ticket for the task of onboarding a new employee.  Title: Onboarding a new employee  Description: We are onboarding a new employee and need to create a Jira ticket for this task. The ticket should include the following information:  -The name of the new employee -The department they will be working in -Any specific onboarding tasks that need to be completed -The date they are starting -The name of the person who will be responsible for onboarding them  This information will help us to create a Jira ticket that will ensure the new employee has a smooth onboarding process.

## self_instruct / command-xlarge / id212: judge 2, MTurk 3.5, Scale 5

**Instruction:** Given a real estate listing description, extract the information and details of the property from the text. The details consist of address, basic house attributes, etc. WALK TO THE BEACH FROM CAPITOLA KNOLLS! Single-level upstairs condo with your own large private deck overlooking nature. Adorable home that is move-in ready and waiting for you to put your own personal touches on. Gorgeous and well-maintained landscaped park-like setting with lush green grasses with a community pool and spa to en

**Output:**  Address: 541 Clares St, Capitola, CA 95010 Bedrooms: 2 Bathrooms: 2 Square feet: 936 Property type: Condo Built: 1972 Garage: 1 car Parking: 1 space Listed for: $899,000  Property details: Walk to the beach from Capitol Knolls! Single-level upstairs condo with your own large private deck overlooking nature. Adorable home that is move-in ready and waiting for you to put your own personal touches on. Gorgeous and well-maintained landscaped park-like setting with lush green grasses with a community pool and spa to enjoy. Desirable location...walk to Capitola Village, Gayle's Bakery, restaurants, shopping, schools or jump on Hwy 1 right around the corner.

## open_assistant / command-xlarge / id3546: judge 2, MTurk 4.5, Scale 4

**Instruction:** I'm an English speaker trying to learn Japanese Kanji using mnemonics. Mnemonics for Kanji are created from the primitives that make them up. The Kanji for Tax has the primitives wheat and devil, so an example would be, "Taxes are like the devil taking away your hard earned wheat". Can you create a mnemonic for the Kanji meaning Wish that has the primitives clock and heart?

**Output:** The clock is ticking, and my heart is with you.

## grammar / command-xlarge / id6: judge 1, MTurk 5, Scale 1.5

**Instruction:** Write a casual message in Greek to my Airbnb host saying I’m going to be a little late to check-in and that I will arrive at 4pm.

**Output:** Με αυτό τον καιρό θα πληρώσω αυτό τον καιρό να πληρώσω τις 4 μ.μ.

## open_assistant / command-xlarge / id3628: judge 1, MTurk 3.5, Scale 3

**Instruction:** Could you provide a brief summary of the book "Fooled by Randomness", by Nassim Nicholas Taleb? Please provide a few paragraphs with the summary and the main points discussed in the book.  How well the book was accepted and was there any negative or positive critic of the work presented there?

**Output:**  Fooled by Randomness is a standalone book in Nassim Nicholas Taleb's landmark Incerto series, an investigation of opacity, luck, uncertainty, probability, human error, risk, and decision-making in a world we don't understand.  The book is the third volume in Taleb's five-volume philosophical essay series, an investigation of opacity, luck, uncertainty, probability, human error, risk, and decision-making in a world we don't understand.  Fooled by Randomness is a standalone book in Nassim Nicholas Taleb's landmark Incerto series, an investigation of opacity, luck, uncertainty, probability, human error, risk, and decision-making in a world we don't understand.  The book is the third volume in 

## grammar / command-xlarge / id17: judge 1, MTurk 1.5, Scale 5

**Instruction:** Translate the following text into Greek: A ship's wheel or boat's wheel is a device used aboard a water vessel to steer that vessel and control its course. Together with the rest of the steering mechanism, it forms part of the helm. It is connected to a mechanical, electric servo, or hydraulic system which alters the horizontal angle of the vessel's rudder relative to its hull. In some modern ships the wheel is replaced with a simple toggle that remotely controls an electro-mechanical or electro

**Output:** Πλέγμα μας είναι ένα σύστημα που χρησιμοποιείται σε πλοίο που βρίσκεται στην θάλασσα για να αναλύσει την κυρία σας και να διασκεδάσει την πλοίο σας. Εκείνη τη στιγμή, συνδυάζει με το resto της κυκλικής συσκευής. Είναι συνδυασμένο με μηχανικό, ελεγχόμενο, ή ανάλυσης ανάλυσης κυλικής σύστημα που αναλύει την ανάλυση του σχέδιου στην αποστολή του σχέδιου στην αποστολή του σχέδιου. Σε μια μικρή πλευρά των νέων σκάφων, το πλέγμα είναι απελευθέντα με ένα απλό μικρού κουτιούχου που αναπτύσσει μια ανάλυση ανάλυσης ανάλυσης κυλικής σύστημα που αναλύει την ανάλυση του σχέδιου στην αποστολή του σχέδιου. Πλέγμα μας είναι ένα σύστημα που χρησιμοποιείται σε πλοίο που βρίσκεται στην θάλασσα για να αναλύσει 


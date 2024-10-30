# Project1
**1. How data is scrapped**
   
The data was collected using the below GitHub APIs 
https://api.github.com/search/users  and https://api.github.com/users/
https://api.github.com/users/{username}/repos 
First did a search for users based in Bangalore with more than 100 followers. Then for each user, retrieved their details from the users' endpoint, ensuring to clean the company names by trimming whitespace, removing leading @ symbols, and converting them to uppercase. Subsequently, fetched up to 500 of their most recently pushed repositories.

**2. The most interesting and surprising fact **
Highly-followed users favor JavaScript, TypeScript, and MIT licenses. Surprisingly, there's a weak link between followers and stars (correlation: 0.024), indicating minimal influence. The cc0-1.0 license leads with the highest average stars (374.7), likely due to standout repositories like "Hack-with-Github/Awesome-Hacking."

**3. An actionable recommendation**
Developers aiming for visibility should prioritize using popular languages (e.g., JavaScript, TypeScript) and the MIT or Apache-2.0 licenses, which are widely adopted by successful users. Focus on creating high-value repositories, as star ratings are driven more by project quality and relevance than follower count

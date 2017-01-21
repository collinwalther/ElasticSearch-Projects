The files here use the reddit submissions API for ElasticSearch to do stuff with reddit data.

Thanks to reddit user <a href = "https://www.reddit.com/user/Stuck_In_the_Matrix">Stuck_In_The_Matrix</a> for providing the API 
<a href = "https://www.reddit.com/r/datasets/comments/5nxkob/reddit_submissions_are_now_in_elasticsearch_and/">here</a>.

Current results I've gotten from my projects:

Average score of all [Poetry] posts on /r/youtubehaiku: 124 
Average score of all [Haiku] posts on /r/youtubehaiku: 120 
Average score of all [Poetry] posts with score >= 20 on /r/youtubehaiku: 383 
Average score of all [Haiku] posts with score >= 20 on /r/youtubehaiku: 387 
Surprisingly, the length of the video doesn't significantly effect how popular it becomes, which is not what I was expecting from 
a userbase which I assume has a very short attention span.  I suppose the videos aren't long enough (max 30 seconds) for it to
make a difference.

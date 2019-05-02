# Groover Music Test Plan

 *****Project Team:***** 

Teresa Ibarra, Siena Guerrero, Trevor Walker, Jocelyn Chen, Walker Quinn

 ***Project Sponsor:***

Harvey Mudd College

## I. Introduction


This serves as the plan for testing all software artifacts as well as the reporting of test results. Our bugs are almost all discovered by inputting different things into our forms. 


## II. Test Plan

| Bug #        | Description   | Expected  | Actual | Fixed? | Solution|
| ------------- |:-------------:| -----:| -----:| -----:| -----:|
| 1     | Lyric-less Song| Crashed model | All lyric-less songs return same recs| Yes| No error. Our model depends on lyric|
| 2     |   Song not in MusixMatch   |  Error | Out of bounds error| Yes| Catch error with try/except. Cannot make recs for those songs|
| 3 |   Song containing #  |  Error | Error| Yes|Remove ‘#’s before processing |
| 4 | Song containing /      | Error | Error| Yes| Same as above|
| 5 | Song containing ‘     | Error | No Error| Yes| Same as above|
| 6 | Other special characters     |   Error | Error| Yes| Catch all special characters that would not be in a song name and return message not to submit special characters|
| 7 | Empty parameters| Error | Error| Yes| Display message to not submit empty parameters|
| 8 | Autofill old input songs     |  | Did not want| Yes| Turn of autocomplete|
| 9 | Overlapped songs don’t align      |     | Did not want| Yes| Fixed CSS|

 



## III. Testing Deliverables


Our testing consisted of testing edge cases in our two input parameters. The HTML/CSS aspects of our website did not require testing – only fixing. We only needed to test the Python and API calls and the model. The edge cases that we tested and found bugs in were recorded in the log above. They have all been fixed. 


## IV. Environmental Requirements


We did not use any tools for debugging. We used only our site for inputting and heroku/local logs for finding source of the error and fixing it. 

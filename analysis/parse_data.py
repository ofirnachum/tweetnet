import json

file = open('r2/tweets.json', 'r');
json_string = "";
for line in file:
    json_string += line;
unparsed_tweets = json.loads(json_string)['tweets'];

# Dictionary mapping username to its tweets
users_tweets = {};
for tweet in unparsed_tweets:
    user = tweet['username'];
    timestamp = int(tweet['timestamp']);
    content = tweet['content'];
    if user not in users_tweets:
        users_tweets[user] = [];
    users_tweets[user].append((timestamp, content));
print "START AND END TIMES";
# Sort tweets by timestamp
for user, tweets in users_tweets.iteritems():
    users_tweets[user].sort();
    print user, ": ", users_tweets[user][0][0], users_tweets[user][-1][0];

# Print tweet count
print "TWEET COUNT";
for user, tweets in users_tweets.iteritems():
    print user, ": ", len(tweets);

# Print hash count
print "HASH COUNT";
for user, tweets in users_tweets.iteritems():
    counts = [0]*16;
    for (time, content) in tweets:
        if (time <= 1399531568) or (time >= 1399531890):
            counts[hash(content) % 16] += 1;
    print user, ": ", max(counts), min(counts), counts;

tol = 15;
for user, tweets in users_tweets.iteritems():
    for i in xrange(len(tweets) - 33):
        #if (hash(tweets[i][1]) % 16 == hash(tweets[i+33][1]) % 16):
        if (1399531568+tol >= tweets[i][0] >= 1399531568 and 1399531719-tol <= tweets[i+32][0] <= 1399531719):
            #print user, i, tweets[i][0] % 1000, tweets[i+32][0] % 1000, hash(tweets[i][1]) % 16
            if (i + 33 + 32 >= len(tweets)):
                continue;
            if (1399531890-tol <= tweets[i + 33 + 32][0] <= 1399531890):
                print "target acquired: ", user, tweets[i][0] % 1000, tweets[i+32][0] % 1000, tweets[i + 33 + 32][0] % 1000;
                for (time, content) in tweets:
                    if (time < tweets[i][0]):
                        if (hash(content) % 16 == hash(tweets[i][1]) % 16):
                            print "whoops, false alarm";

asdfasdf

# Print average word per tweet
print "WORD AVERAGE";
for user, tweets in users_tweets.iteritems():
    total_words = sum([len(content.split(" ")) for (time, content) in tweets]);
    average_words = total_words / len(tweets);
    print user, ": ", average_words;

# Print most common words
print "COMMON WORDS";
from collections import Counter
for user, tweets in users_tweets.iteritems():
    all_words = sum([content.lower().split(" ") for (time, content) in tweets], []);
    common_words = Counter(all_words);
    print user, ": ", common_words.most_common(10);

# Print number of character
chars = ['http://', ' ', '@', '#'];
print "AVERAGE NUMBER OF OCCURENCES OF: '" + str(chars) + "'";
for user, tweets in users_tweets.iteritems():
    print user, ": ", 
    for char in chars:
        num_occurences = sum([content.count(char) for (time, content) in tweets]);
        print float(num_occurences) / len(tweets), " ",
    print "\n",

# Print proportion alphabet and digit characters
print "ALPHABET AND DIGIT PROPORTIONS: ";
for user, tweets in users_tweets.iteritems():
    num_alpha = sum([sum([x.isalpha() for x in content]) for (time, content) in tweets]);
    num_digit = sum([sum([x.isdigit() for x in content]) for (time, content) in tweets]);
    num_alnum = sum([sum([x.isalnum() for x in content]) for (time, content) in tweets]);
    total_char = float(sum([len(content) for (time, content) in tweets]));
    print user, ": ", (num_alpha / total_char), " ", (num_digit / total_char), " ", (num_alpha / total_char);

# Print num tweets in each window
print "TIME WINDOWS:"
time_window = 40;
for user, tweets in users_tweets.iteritems():
    windows = {};
    for tweet in tweets:
        if (tweet[0] // time_window not in windows):
            windows[tweet[0] // time_window] = 0;
        windows[tweet[0] // time_window] += 1;
    windows_list = sorted(windows.items());
    print user, " ", windows_list;

# Print number of misspelled words
print "MISSPELLED WORDS: "
file = open("/usr/share/dict/words", "r");
english = {};
for line  in file:
    english[line.strip().lower()] = True;
for user, tweets in users_tweets.iteritems():
    total_words = 0;
    misspelled = 0;
    for time, tweet in tweets:
        for word in tweet.split():
            if (word != ""):
                if (word.lower() not in english and word != "RT"):
                    misspelled += 1;
                total_words += 1;
    print user, " ", float(misspelled) / total_words;

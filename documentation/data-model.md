## Overview  

This document describes the Shapes data tables that exist so far, sketches the tables that don't yet exist, and describes the workflow for populating and using the data.

The model is organized into two categories of data tables. Tables listed under "Application Data" contain the data required by user-facing Shapes applications, and tables under "Session and User Data" contain the data generated by those applications. Some Application Data is informed by analyzing Session and User Data.


**Application Data**  
- [Source Data](#source-data)  
- [Song Data](#song-data)
- [Source-Song Join Table](#source-song-join-table)
- [Multi-song Videos](#multi-song-videos)   
- [Manual Video Metadata](#manual-video-metadata)  
- [Video Zoom](#video-zoom)  
- [Automatic Video Metadata](#automatic-video-metadata)  
- [Key Level Context](#key-level-context)  
- [Chord Level Context](#chord-level-context)  
- [Curation](#curation)  
- [Audio Data](#audio-data)  
- [Default Instrument Settings](#default-instrument-settings)  
- [Original iPad App Instrument Settings](#original-ipad-app-instrument-settings)  

**Session and User Data**  
- [Session Data](#session-data)  
- [User Key Level Context](#user-key-level-context)  
- [User Chord Level Context](#user-chord-level-context)  
- [User Comments](#user-comments)  
- [User Song Preference](#user-song-preference)  
- [User Song Rating](#user-song-rating)  
- [Event Data](#event-data)  

**API Workflow**
- [Maintain a list of sources](#maintain-a-list-of-sources)  
- [Add Songs](#add-songs)  
- [Add YouTube Video IDs](#add-youtube-video-ids)  
- [Crawl YouTube Metadata](#crawl-youtube-metadata)  
- [Retrieve One-Time YouTube Metadata](#retrieve-one-time-youtube-metadata)  
- [Download Music Video Files to the server](#download-music-video-files-to-the-server)
- [Input Manual Video Metadata](#input-manual-video-metadata)
- [Play Videos as fullscreen background](#play-videos-as-fullscreen-background)
- [Play a Browser Instrument over Video Background](#play-a-browser-instrument-over-video-background)
- [Automatically Analyze Tuning and Key Context](#automatically-analyze-tuning-and-key-context)  
- ...


---
## Application Data
This is the data required by user-facing Shapes applications.


### Source Data  
The `source` model describes the source (e.g. a chart, playlist, article, etc.) from which songs were added to the database.

source ||
--- | --- |
`id` | `integer`<br> The `id` for the source. |
`parent_entity` | `text`<br> The organization, publication, institution, etc. from which the source originated. |
`parent_stream` | `text`<br> The recurring series, feed, channel, etc. where the source was published. |
`instance_name` | `text`<br> The published instance of the source. |
`publication_date` | `numeric`<br> The publication date displayed on the source (this is not necessarily the actual release date). |
`location` | `text`<br> The URL of the source instance at the time it was added to the database. |

```sql
--Schema

CREATE TABLE source (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  parent_entity TEXT,
  parent_stream TEXT,
  instance_name TEXT,
  publication_date NUMERIC, --DATETIME
  location TEXT
);
```
```json
/* Example record */

{
 "id" : 1,
 "parent_entity" : "Complex",
 "parent_stream" : "Best New Music This Week",
 "instance_name" : "Brockhampton, Vince Staples, Lana Del Rey, and More",
 "publication_date" : "2019-08-23 00:00:00.000000",
 "location" : "https://www.complex.com/music/best-new-music-this-week-brockhampton-vince-staples-lana-del-rey"
}
```


### Song Data
The `song` model describes a unique song added to the database.

song ||
--- | --- |
`id` | `integer`<br> The unique `id` for the song. |
`title` | `text`<br> The title of the song. |
`artist_name` | `text`<br> The name of the artist or artists, prior to artist deduplication or cleanup. |
`video_id` | `text`<br> The YouTube video ID. |

```sql
--Schema

CREATE TABLE song (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  title TEXT,
  artist_name TEXT,
  video_id TEXT
);

CREATE TRIGGER new_meta_row AFTER INSERT ON song  
BEGIN  
  INSERT INTO video_metadata(song_id)
  VALUES (NEW.id);  
END;

CREATE TRIGGER new_curation_row AFTER INSERT ON song  
BEGIN  
  INSERT INTO curation(song_id)
  VALUES (NEW.id);  
END;

-- temporary

CREATE TRIGGER new_comment_row AFTER INSERT ON song  
BEGIN  
  INSERT INTO comment(song_id)
  VALUES (NEW.id);  
END;

CREATE TRIGGER new_user_pref_row AFTER INSERT ON song  
BEGIN  
  INSERT INTO user_preference(song_id)
  VALUES (NEW.id);  
END;

CREATE TRIGGER new_user_rating_row AFTER INSERT ON song  
BEGIN  
  INSERT INTO user_rating(song_id)
  VALUES (NEW.id);  
END;
```
```json
/* Example record */

{
	"id" : 1,
	"title" : "St. Percy",
	"artist_name" : "Brockhampton",
	"video_id" : "rp-I-YGg6Hs"
}
```


### Source-Song Join Table
The `source_song` table allows many-to-many relationships between sources and songs.

source_song ||
--- | --- |
`id` | `integer`<br> The unique `id` for the source-song reference. |
`capture_date` | `numeric`<br> The date the song instance was added to the database. |
`source_id` | `integer`<br> A reference to the `source` the song was added from. |
`song_id` | `integer`<br> A reference to the unique `song` added. |

```sql
--Schema

CREATE TABLE source_song (
   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
   capture_date NUMERIC, --DATETIME
   source_id INTEGER,
   song_id INTEGER,
   FOREIGN KEY(source_id) REFERENCES source (id),
   FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```json
/* Example record */

{
	"id" : 1,
	"capture_date" : "2020-05-04 21:25:11.000000",
  "source_id" : 1,
	"song_id" : 1
}
```


### Multi-song Videos
The `multisong_vid` table tracks `video_ids` that are valid duplicates.

multisong_vid ||
--- | --- |
`id` | `integer`<br> The unique `id` for the valid match. |
`video_id` | `text`<br> The YouTube video ID for the multi-song video. The count of unique `video_ids` in this table gives the valid duplicate count for each `video_id`. |
`song_id` | `integer`<br> The unique `id` for each song that corresponds to a multi-song video. |

```sql
--Schema

CREATE TABLE multisong_vid (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  video_id TEXT,
  song_id INTEGER,
  FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```json
/* Example record */

{
	"id" : 1,
	"video_id" : "0jz0GAFNNIo",
	"song_id" : 369
}
```


### Manual Video Metadata
The `video_metadata` model describes metadata that needs some help from a human to fill in.

video_metadata ||
--- | --- |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`has_video` | `boolean`<br> Indicates whether the `video_id` has a music video that places you in a world. |
`check_back` | `boolean`<br> Flags a video to check back later for a possible update to the `video_id` and `has_video`. For example, if a lyric video seems likely to be replaced soon by an official video. |
`start_time` | `numeric`<br> The time one second before the second when music begins (to trim non-music intros). This is input as displayed on YouTube, and converted to seconds in the player. |
`end_time` | `numeric`<br> The time one second after the second when the song ends (to trim non-music outros). This is input as displayed on YouTube, and converted to seconds in the player. |
`release_year` | `integer`<br> The year the song was first released, which may be different from the year it was published to YouTube. Can take a little research, especially for older songs. |

```sql
--Schema

CREATE TABLE video_metadata (
  song_id INTEGER,
  has_video NUMERIC,
  check_back NUMERIC,
  start_time NUMERIC, -- TIME
  end_time NUMERIC, -- TIME
  release_year INTEGER,
  FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```json
/* Example record */

{
	"song_id" : 5643,
	"has_video" : "N",
	"check_back" : "Y",
  "shelf_life" : "N",
  "start_time" : "0:00:00",
  "end_time" : "0:02:42",
  "release_year" : 2013
}
```


### Video Zoom
The `video_zoom` model describes data needed to scale the active video content (inside letterboxing) to fill the browser window.

video_zoom ||
--- | --- |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`video_width` | `integer`<br> The pixel width of active video content within the video file (inside letterboxing), or a pixel width that yields the correct aspect ratio relative to `video_height`. |
`video_height` | `integer`<br> The pixel height of active video content within the video file (inside letterboxing), or a pixel height that yields the correct aspect ratio relative to `video_width`. |
`x_offset` | `integer`<br> A pixel value based on `video_width` to correct active video content that is not centered on the x axis (uncommon).
`y_offset` | `integer`<br> A pixel value based on `video_height` to correct active video content that is not centered on the y axis (uncommon).

```
--Schema

/* Example record */
```


### Automatic Video Metadata
The `yt_data_onetime` model describes video metadata updated once from the YouTube Data API.

yt_data_onetime ||
--- | --- |
`video_id` | `text`<br> The YouTube video ID. Used to reference the song(s) that use this video. |
`dl` | `boolean`<br> Indicates whether there is a copy of the video file on the Shapes server. |
`yt_publication_date` | `numeric`<br> The date the video was published to YouTube. This often (but not always) indicates a song's release date. |
`duration` | `text`<br> The length of the video represented as a Bergsonian... wait, no, as an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) duration. |
`iframe_width` | `integer`<br> YouTube's recommended iframe width. This is the closest we can get to YouTube's file `widthPixels` and `aspectRatio`, which are only visible to the video owner. |
`iframe_height` | `integer`<br> YouTube's recommended iframe height in pixels. This is the closest we can get to YouTube's file `heightPixels` and `aspectRatio`, which are only visible to the video owner. |
`file_width` | `integer`<br> The pixel width of the downloaded video file. This can be used to calculate the aspect ratio of the file, which does not necessarily correspond to the aspect ratio of the active video content (inside letterboxing). |
`file_height` | `integer`<br> The pixel height of the downloaded video file. This can be used to calculate the aspect ratio of the file, which does not necessarily correspond to the aspect ratio of the active video content (inside letterboxing). |

```
--Schema

/* Example record */
```


The `yt_data_recurring` model describes video metadata updated regularly from the YouTube Data API.

yt_data_recurring ||
--- | --- |
`video_id` | `text`<br> The YouTube video ID. Used to reference the song(s) that use this video. |
`yt_exists` | `boolean`<br> Indicates if the video is currently available on YouTube (not removed). |
`yt_view_count` | `integer`<br> The number of YouTube views. |
`yt_regions_allowed` | `text`<br> Regions where the video is explicitly allowed. A video is available in your local region if: a) your region appears in this list; or b) your region does *not* appear in `yt_regions_blocked`; or c) your region does not appear in either list. |
`yt_regions_blocked` | `text`<br> Regions where the video is explicitly blocked. A video is available in your local region if: a) your region does *not* appear in this list; or b) your region appears in `yt_regions_allowed`; or c) your region does not appear in either list. |
`yt_age_restricted` | `boolean`<br> Indicates videos where YouTube displays the alert: "This video may be inappropriate for some users." and requires user agreement. |

```
--Schema

/* Example record */
```


### Key Level Context  
The `key_context` model interprets [`user_key_context`](#user-key-level-context) user data. References `song_id` rather than `session_id`.

```
--Schema

/* Example record */
```


### Chord Level Context  
The `chord_context` model interprets [`user_chord_context`](#user-chord-level-context) user data. References `song_id` rather than `session_id`.

```
--Schema

/* Example record */
```


### Curation
The `curation` model describes data for determining which songs to include or feature.

curation ||
--- | --- |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`featured` | `boolean`<br> Indicates if the song is a Shapes featured song. This is the kind of song you'd want to be your first experience with Shapes, and that's timeless or iconic enough to fit in with a playlist of mostly current songs. Or a song you want to get more use data on. |
`shelf_life` | `boolean`<br> Indicates if the song is temporally bounded to a specific event, and not just to the stylistic qualities of its era. |
`curate_out` | `boolean`<br> Indicates songs that do not fit with the curatorial values of the playlist, but that remain in the database. |

```sql
--Schema

CREATE TABLE curation (
  song_id INTEGER,
  featured NUMERIC,
  shelf_life NUMERIC,
  curate_out NUMERIC,
  FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```json
/* Example record */

{
  "song_id" : 4039,
  "featured" : NULL,
  "shelf_life" : NULL,
  "curate_out" : NULL
}
```


### Audio Data
The `audio` model describes audio attributes of the song relevant to player and instrument settings.

audio ||
--- | --- |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`tuning` | `integer`<br> The frequency to which the note "La" is assigned (standard 440).
`volume` | `integer`<br> The volume/gain profile for the song.
`timbre` | `text`<br> The timbral profile for the song. Something like an EchoNest valence. Looking forward to figuring out exactly what this means, but will be related to choosing instrument timbres that sound good with the song.

```
--Schema

/* Example record */
```


### Default Instrument Settings
The `instrument` model describes settings for a default browser instrument yet to be built.

instrument ||
--- | --- |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`tuning_offset` | `integer`<br> A frequency offset from `audio.tuning`. |
`temperament` | `text`<br> The tuning system to use (default is *Equal Temperament*). Calculates from `anchor` note when necessary. Also potentially describes the tuning system used in the song. |
`transposition` | `integer`<br> A semitone offset from the `audio.tuning` note ("La"). |
`preset` | `text`<br> The default timbral preset for the song. Potentially related to the song's timbral profile described by `audio.timbre`. |
`volume` | `integer`<br> The default volume setting for the instrument, based on the `preset`. Ideally, volume is ignostic to the choice of `preset`. Potentially related to the song's volume profile described by `audio.volume`. |

```
--Schema

/* Example record */
```


### Original iPad App Instrument Settings
The `ipad_instrument` model describes settings for the sampler instrument included in the original Shapes iPad App from 2012-2013.

ipad_instrument ||
--- | --- |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`preset` | `text`<br> The default of five sampler instrument sounds in the original app. May reflect an overall timbral profile for the song. |
`volume` | `integer`<br> The default volume setting for the sampler, based on the `preset`. May reflect an overall volume/gain profile for the song. |

```
--Schema

/* Example record */
```


---
## Session and User Data  
This is the data generated by user-facing Shapes applications.


### Session Data
The `session` model identifies which song was played, when it was played, and the application and user context for the play. A session corresponds to a single song play.

session ||
--- | --- |
`id` | `integer`<br> The unique `id` for the session. |
`song_id` | `integer`<br> A reference to the song (not the `video_id`, since it's possible for one video to contain multiple songs). |
`start` | `numeric`<br> The UTC timestamp when the player loads a new song.  |
`end` | `numeric`<br> The UTC timestamp when the session ends. This may be a) when the user skips to a new song, b) when the song reaches its specified `end_time`, or c) when the application quits. |
`app` | `text`<br> The name of the application (or page view, etc.) that generated the session. |
`user` | `text`<br> A unique username chosen by the user. |

```
--Schema

/* Example record */
```


### User Key Level Context
The `user_key_context` model contains user data to inform the [`key_context`](#key-level-context) table.

user_key_context ||
--- | --- |
`session_id` | `integer`<br> A reference to the song session. |
`single_shape` | `text`<br> Indicates if the song matches convincingly with a single shape, and gives the best match. Otherwise, indicates that the song is a `MULTI` (multi-shape) song. |
`single_anchor` | `text`<br> Indicates if the song matches convincingly with a single anchor, and gives the best match. Otherwise, indicates that the song is a `MULTI` (multi-anchor) song. |
`multi_shapes` | `object`<br> Indicates key-level shape changes within the song. Each change defines:  <br>- the `timestamp` within the video when the change takes place, and <br>- the `shape` that corresponds to the `timestamp`. |
`multi_anchors` | `object`<br> Indicates key-level anchor changes within the song. Each change defines:  <br>- the `timestamp` within the video when the change takes place, and <br>- the `anchor` that corresponds to the `timestamp`. |

```
--Schema

/* Example record */
```


### User Chord Level Context
The `user_chord_context` model contains user data to inform the [`chord_context`](#chord-level-context) table.

user_chord_context ||
--- | --- |
`session_id` | `integer`<br> A reference to the song session. |
`bass_notes` | `object`<br> Indicates chord-level bass note changes within the song. Each change defines:  <br>- the `timestamp` within the video when the change takes place, and <br>- the `bass_note` that corresponds to the `timestamp`. |
`shapes` | `object`<br> Indicates chord-level shape changes within the song, if different from key-level shapes. Each shape change defines:  <br>- the `timestamp` within the video when the change takes place, and <br>- the `shape` that corresponds to the `timestamp`. |
`root_notes` | `object`<br> Indicates chord-level root note changes within the song, if different from `bass_notes`. This introduces the idea of "function." Each change defines:  <br>- the `timestamp` within the video when the change takes place, and <br>- the `root_note` that corresponds to the `timestamp`. |

```
--Schema

/* Example record */
```


### User Comments  
The `user_comment` model contains user comments and interaction notes.

user_comment ||
--- | --- |
`session_id` | `integer`<br> A reference to the song session. |
`comment` | `text`<br> The text of the comment. |
`video_time` | `numeric`<br> The video timestamp that corresponds to the comment. |
`utc_time` | `numeric`<br> The UTC timestamp that corresponds to the comment. |

```sql
--Schema

CREATE TABLE comment (
  song_id INTEGER,
  davidforrest TEXT,
  markforrest TEXT,
  FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```
/* Example record */
```


### User Song Preference
The `user_preference` model contains data indicating which songs a user prefers.

user_preference ||
--- | --- |
`session_id` | `integer`<br> A reference to the song session. |
`interesting` | `boolean`<br> Indicates that the user finds the song interesting, musically or otherwise. A way of flagging songs. Can also indicate if the user finds a song disinteresting, or dislikes the song. |
`selected` | `boolean`<br> The user has loaded the song intentionally (such as by choosing "play previous"). |
`skip_time` | `numeric`<br> Indicates if the user skipped the song, and provides a timestamp within the video. |

```sql
--Schema

CREATE TABLE user_preference (
  song_id INTEGER,
  interesting NUMERIC,
  selected NUMERIC,
  skip_time NUMERIC,
  FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```
/* Example record */
```


### User Song Rating
The `user_rating` model describes data indicating user opinions about song rating.

user_rating ||
--- | --- |
`session_id` | `integer`<br> A reference to the song session. |
`feels` | `integer`<br> An affect rating. On a scale of 1-100, how does this song make you feel? |
`explicit` | `boolean`<br> Indicates if the song is explicit overall, whether or not it contains any of the fields below. |
`language` | `integer`<br> On a scale of 1-100, does the song contain strong language? A standard MPAA / RIAA category. |
`violence` | `integer`<br> On a scale of 1-100, does the song contain depictions of violence? A standard MPAA / RIAA category. |
`sex` | `integer`<br> On a scale of 1-100, does the song contain depictions of sex? A standard MPAA / RIAA category. |
`substance` | `integer`<br> On a scale of 1-100, does the song contain depictions of substance use/abuse? A standard MPAA / RIAA category. |
`occult` | `integer`<br> On a scale of 1-100, does the song transgress normative religious or scientific beliefs? From Tipper Gore's PMRC, included here for fun. |
`kids` | `boolean`<br> Indicates that the song may be especially interesting or well-suited for kids. |

```sql
--Schema

CREATE TABLE user_rating (
  song_id INTEGER,
  feels NUMERIC,
  explicit NUMERIC,
  language NUMERIC,
  violence NUMERIC,
  sex NUMERIC,
  substance NUMERIC,
  occult NUMERIC,
  kids NUMERIC,
  FOREIGN KEY(song_id) REFERENCES song (id) ON DELETE CASCADE
);
```
```
/* Example record */
```


### Event Data
The `event` model describes instrument (MIDI) notes or durationless (timestamp) events, such as pulse markers.

event ||
--- | --- |
`session_id` | `integer`<br> A reference to the song session. |
`start_video` | `integer`<br> The video timestamp that corresponds to the event start. |
`start_utc` | `integer`<br> The UTC timestamp that corresponds to the event start. |
`end_video` | `integer`<br> The video timestamp that corresponds to the event end. |
`end_utc` | `integer`<br> The UTC timestamp that corresponds to the event end. |
`midi_note` | `integer`<br> The MIDI note number of the event. |
`velocity` | `integer`<br> The MIDI velocity of the event. |

```
--Schema

/* Example record */
```


---
## API Workflow  


### Maintain a list of sources
Application: [`Song-Scraper`](https://github.com/davidforrest/Song-Scraper)

- Maintain the list within the application used for adding songs, currently, in the `README.md` file.

### Add Songs
Application: [`Song-Scraper`](https://github.com/davidforrest/Song-Scraper)

**Scrape from a recurring source**

- Work down the Recurring Sources list, one source at a time.
- For each source, open the chart link and scraper code, and follow steps in the code.
- In this process, songs are **checked for duplicates** before adding.
- The `video_id` is included in some scrapers, but not all.
- [Here's a video](https://drive.google.com/file/d/1iJciScKJulp1BurPt_GT1cboh_W1eSLO/view) of what this process looks like.

**Manually add single songs and non-recurring sources**

- Open `manual-add.js` and follow steps in the code.
- As for recurring sources, manual additions are checked for duplicates and logged in `source-song`.


### Add YouTube Video IDs
Application: SQLite Studio

- Open the `playlisting` view in SQLite Studio.
- This displays metadata fields from multiple tables, sorted first by `check_back`, then by songs with no `video_id`.
- Copy-Paste `title` and `artist_name`, into a YouTube search
- Find the "official" or best quality video. Prioritize results that have music videos. It's sometimes helpful to sort by viewcount.
- Copy-Paste the video ID into the `video_id` field  
- Mark if `has_video`
- Optionally add any other metadata or notes.
- Commit changes in SQLite Studio

**Delete a song from the db**

- Sometimes while adding a video, you realize you don't actually want that song in the database.
- Delete the song's row from the `song` table. An `ON DELETE CASCADE` is set up on foreign keys that point to the `song` table, so rows in other tables that reference the deleted `song_id` will be deleted, too.

**Multi-song Videos**

- Sometimes a single `video_id` will contain multiple songs.
- In these (rare) cases, add the duplicate `video_id` to each song, then manually create entries for each song in the `multisong_vid` table.
- The purpose of the `multisong_vid` table is to distinguish cases like these from duplicate songs in the database.

---

### Crawl YouTube Metadata

- regularly and automatically update YouTube data that's subject to change:
    - `yt_exists`
    - `yt_view_count`
    - `yt_regions_allowed`
    - `yt_regions_blocked`
- ok to overwrite prior values rather than tracking how this data changes over time? that seems a bit outside the focus of this project.


### Retrieve One-Time YouTube Metadata

- automatically populate the YouTube data that's unlikely to change:
    - `yt_age_restricted` (could this change?)
    - `yt_publication_date`
    - `duration`
    - `iframe_width`
    - `iframe_height`


### Download Music Video Files to the server

- only download songs that exist according to recent YouTube Metadata
- using [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- had been using a .txt file listing all `video_id` to be downloaded, with the following quality settings:  
```
youtube-dl -a song_list.txt -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' --id
```
- update `dl` field
- update `dl_width` and `dl_height` fields in Automatic Video Metadata
- check downloaded files against unique `video_id`s (to replace videos, for example, that were removed or blocked before we downloaded them)


### Input Manual Video Metadata

- the manual updates that aren't music-related:
    - `has_video`
    - `start_time`
    - `end_time`
    - `release_year`
- also includes video zoom until that can be automated
- as when adding `video_id`, optionally add any other metadata or notes. this is the sort of "music criticism" step--it needs some more definition and a place to live.

### Play Videos as fullscreen background

- Filter videos for:
    - `video_id` is defined
    - available on YouTube in your region
    - `has_video`
    - published or added within a date range
    - etc.

Let's think about video zoom for a moment. What we're really doing is:
- laying a div over the video that matches the active content size  
- adjusting the video on the x & y axis beneath that div if necessary  
- scaling the div (and its contents) to fill the browser window (based on the shortest side?)


### Play a Browser Instrument over Video Background

- set default settings
- collect user settings to inform default settings (manually set tuning, instrument timbre, etc.)
- potentially use [websynths.com](https://websynths.com/) as inspiration?
- potentially make use of the default instrument and volume settings from the original iPad app?


### Automatically Analyze Tuning and Key Context

- Klaus [prototyped](https://gitlab.com/vltmrkls/shapes-detection) a shape detection that could (potentially) crawl over the downloaded video files.
- [tONaRT](http://www.zplane.de/index.php?page=description-tonart) and others can detect the tuning and Major/minor key, which a human could verify.
- ideally this kind of analysis would happen between music start and end times, or other time ranges defined elsewhere in the data

1)Introduction:
	This is a basic application of API Calls using the Spotify API.

2)About authorization:
	The authorization technique used is Client Credentials Flow. It provides with an access token for an hour and need to get another if one wants to continue. Other techniques are also present to experiment(Authorization Code Flow,  Authorization Code Flow With Proof Key for Code Exchange (PKCE), Implicit Grant)

	For more information on differences between them: https://dzone.com/articles/the-right-flow-for-the-job-which-oauth-20-flow-sho 

3)About functions:
	The functions allows the client to search for an artists top tracks, search for an album and tracks based on specified genre.
	To instantiate the class it accepts two compulsory arguments client_id and client_secret. 
	In class SpotifyAPI, the function authentication performs authorization and recieves the access token, which is required for all further api calls.
	The  function get_tracks_of_artists(artist_name, country_code) accpets two arguments 'artist_name' and 'country_code', country_code should be in ISO_3166-2_alpha_country_code format. This function returns a list of provided artist's songs in the form of list.
	The function get_tracks_based_on_genres(genre, artist) accepts two arguments, one compulsory argument 'genre' and optional argument 'artist', where artist should be the artist_name. This function returns a list of tracks based on genre provided.
	The search(query, search_type, operator, operator_query) function takes four arguments, two compulsory arguments 'query' and 'search_type', 'search_type' can be artist/album/track and 'query' should be in accordance to the search_type and two optional arguments 'operator' and 'operator_query' where 'operator' can be 'OR' or 'NOT' and 'operator_query' should be a query supporting 'operator'.It returns a json file.
	Ex.search(query='Danger', search_type='albums', operator='NOT', operator_query='Billie Ellish')
	This function performs search for albums having Danger in their name and not produced by 'Billie Ellish'
	('operator' and 'operator_query' are optional arguments)
	

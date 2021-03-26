# Tradier-Python API

[readthedocs](https://pytradierdevelopment.readthedocs.io/en/latest/)

# Current Philosophy

The main idea of the project is to create a python wrapper around the Tradier platform.
This package aims to be concise, straightforward, and flexible for practioners to use in
any setting. At the moment, the current project simply seeks to cover the simple basics for interaction with the API, including account settings, watchlists, market data, trading, and streaming. Each module intends to stand on its own, for users to decide when functions are most helpful to them.

## Testing Issues

Currently the testing is still calling the "v1/user/profile" endpoint in real life because the base object that all other objects are inheriting from calls that endpoint on initialization. Not sure how important that is yet, but right now when testing the fundamental data it is leading error being printed when initializing the FundamentalData object as a non paper account. Tests still pass, since afterward the requests.get function is mocked, but something to keep in mind.

## Implementation Details

## Future Releases

- algorithmic traders interested in using this platform will prioritize speed as a requirement for success. Re-implementing code as asynchronous is on the roadmap

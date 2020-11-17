# HowBusyIsToon.com

This website was developed as a collaboration involving Newcastle University, Hedgehog Lab, MHCLG and Newcastle City Council.

Its development was part-funded by the [Local Digital Fund](https://localdigital.gov.uk/fund/).

The current version of the live website can be viewed at [HowBusyIsToon.com](http://www.howbusyistoon.com/).   

## Development

[Hugo](https://gohugo.io/), the static site generator, is used to generate the HTML content. You can install this on your own machine and run `hugo` in the `web/` directory, which will create a `public` directory of the content.

Refer to the Hugo documentation for additional options for development purposes.

A development [compose](a) stack is also available. To run it, use:
```bash
docker-compose -f docker-compose.dev.yml up
``` 

## Deployment

The Urban Observatory runs this site under Traefik. Deployment on our systems is performed by running:
```bash
docker-compose up
```

A Google Maps API key is required. Set this in the `.env` file, such as
```
HUGO_PARAMS_googleMapsKey=your_key_goes_here
```

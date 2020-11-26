var vue = new Vue({
    el: '#app',
    data: {
      videoImage1: null,
      videoImage2: null,
      header: null,
      headerhighlight: null,
      callout: null,
      isMobileShowing: false,
      calloutClass: null,
    },
    methods: {
      onLoad: function() {
        this.intervalId = setInterval(async () => {
          await this.getVideoImage();
        }, 300000) // 5 minutes
      },
      getVideoImage: async function() {
        var res = await await axios.get('https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/timeseries/b0cf0739-8bf0-4edc-83ff-99be42d0dc21');
        if (res.status = 200) {
          this.videoImage1 = res.data.latest.value;
        }
        res = await await axios.get('https://api.newcastle.urbanobservatory.ac.uk/api/v2/sensors/timeseries/685e0b8e-9c97-41df-94db-c039205814d1');
        if (res.status = 200) {
          this.videoImage2 = res.data.latest.value;
        }
      },
      getCityState: async function() {
        return await axios
          .get('/ncc-city-state.json');
      },
      getParking: async function() {
        return await axios
          .get('/ncc-car-parks.json');
      },
      setHeaderText: function(data)
      {
          if(data.state.city_state === 'busy') {
            this.header = 'Lots of people are visiting the city centre right now.';
            this.headerhighlight = 'You may find social distancing easier at a different time.';
            this.calloutClass = "callout--red";
          } else if (data.state.city_state === 'average') {
            this.header = 'People are out and about in the city centre right now.';
            this.headerhighlight = 'Social distancing is possible in many areas but not all.';
            this.calloutClass = "callout--orange";
          } else {
            this.header = 'There are not many people in the city centre right now.';
            this.headerhighlight = 'Social distancing should be easy.';
            this.calloutClass = "callout--green";
          }
      },
      map: function(data) {

        let stateColour = '#28A746';
        
        if(data.state.city_state === 'busy') {
            stateColour = '#DC3545';
        } else if (data.state.city_state === 'average') {
            stateColour = '#FFC107';
        } else {
        }
        console.log(stateColour);
        
        const map = L.map('map', { zoomControl: false, maxZoom: 16 }).setView([54.9759, -1.6128], 15);
    
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        }).addTo(map);
    
        L.control.zoom({
            position:'topright'
        }).addTo(map);
    
        var northEnd = new L.LatLng(54.977758, -1.613620);
        var midPoint = new L.LatLng(54.975865, -1.612830);
        var southEnd = new L.LatLng(54.974312, -1.611817);
        var pointList = [northEnd, midPoint, southEnd];
    
        var line = new L.Polyline(pointList, {
            color: stateColour,
            weight: 5,
            opacity: 0.75,
            smoothFactor: 1
        });
        
        // line.addTo(map);

        var capacity = 0;
        var filled = 0;
    
        carparks.forEach(function(carpark){
    
            const currentData = data.carparks.carparks.find(obj => { return obj.name === carpark.name; });
            const spaces = currentData ? (carpark.capacity - currentData.occupancy) : carpark.capacity;
            const state = currentData ? currentData.state : 'unknown';

            if (currentData) {
              capacity = capacity + carpark.capacity;
              filled = filled + currentData.occupancy;
            }
            
            let popupMessage = '';
            
            if(currentData) {
                popupMessage = 'There are ' + spaces + ' spaces remaining at ' + carpark.name + '.';
            } else {
                popupMessage = 'There are a total of ' + spaces + ' spaces at ' + carpark.name + '.';
            }
    
            const marker = L.divIcon({
                html: '<img alt="marker-' + state + '" src="assets/images/map-marker-' + state + '.png"><span class="spaces">' + spaces + '</span>',
                iconSize: [60, 60],
                iconAnchor: [30, 60],
                className: 'car-park-marker'
            });
    
            if(carpark.location.length === 2) {
                L.marker(carpark.location, { icon: marker }).addTo(map)
                .bindPopup(popupMessage);
            }
        });
        if (capacity != 0)
        {
          var perc = 100 * filled / capacity;
          // Disabled because might be misleading - LS 24 Nov 2020
          // this.callout = "Car parks at " + Math.round(perc) + "% capacity."
          this.callout = "Check our map below for car parking spaces."
        } else {
          this.callout = "Check our map below for car parking spaces."
        }
      }
    },
    async mounted () {
      if (window.location.pathname === '/') {
        await this.getVideoImage();
        this.onLoad();
      }
      
      var data = {};
      var state = await this.getCityState();
      console.log(state);
      if (state.status == 200) {
        data.state = state.data;
        this.setHeaderText(data);
      }
      if (window.location.pathname === '/parking.html') {
        var parking = await this.getParking();
        console.log(parking);
        if (state.status == 200 && parking.status == 200) {
          data.carparks = parking.data;
          console.log(data);
          this.map(data);
        }
      }
    },
    beforeDestroy() {
      if (window.location.pathname === '/') {
        clearInterval(this.intervalId)
      }
    }
});

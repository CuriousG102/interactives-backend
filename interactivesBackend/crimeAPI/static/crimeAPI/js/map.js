var CrimeMap = {
    DEFAULT_COLOR: "rgb(255,255,178)",
    BORDER_COLORS: "#000",
    CHORO_COLORS: ['rgb(254,217,118)','rgb(254,178,76)',
                   'rgb(253,141,60)','rgb(240,59,32)',
                   'rgb(189,0,38)'], // http://colorbrewer2.org/
    TRACT_DEFAULT_COLOR: 'rgb(255,255,204)',
    TRACT_CHORO_COLORS: ['rgb(199,233,180)','rgb(127,205,187)',
                         'rgb(65,182,196)','rgb(44,127,184)',
                         'rgb(37,52,148)'],
    NO_AREA_VALUES_TEXT: 'Unfortuntately, there is not enough data to color the map for this date range',
    NO_TRACT_VALUES_TEXT: 'Unfortunately, there is not enough data to color the map at this detail level for this date range',
    svg: null,
    area_tracts: [],
    areas_active: false,
    tracts_active: false,
    areas_legend_numbers: null,
    tracts_legend_numbers: null, // these two are arrays that hold the upper thresholds for colors given via our legend
    previous_area: null, // the area that we were previously zoome in on,
                         // stored as an instance variable so we can zoom
                         // in on the next area while setting other areas
                         // to not be classed as active in O(1) rather than
                         // O(n)
    tract_crime_numbers: {},
    MAP_RATIO: 0.75,
    projection: null,
    path: null,
    geojson: null,

    plotLegend: function(isArea) {
        var legendBox = d3.select("#mapLegend").html("");

        var makeLegend = function(shades, legend_numbers) {
            var colorNumbers = [];
            colorNumbers.push({color: shades[0],
                               text: "0 crimes"});
            colorNumbers.push({color: shades[1],
                               text: "1 to " + 
                               Math.ceil(legend_numbers[0]) +
                               " crimes"});

            for (var i = 1; i < shades.length - 1; i++) {
                var text = [Math.ceil(legend_numbers[i- 1]),
                            "to", 
                            Math.ceil(legend_numbers[i]),
                            "crimes"].join(" ");
                colorNumbers.push({color:shades[i+1],
                                   text: text});
            }

            var legendEntriesEnter = legendBox.selectAll(".legendEntry")
                                            .data(colorNumbers)
                                            .enter()
                                            .append("div")
                                            .attr("class", "legendEntry");

                    
            legendEntriesEnter.append("div")
                            .attr("class", "legendEntryColor")
                            .style("background", function(d){return d.color;});

            legendEntriesEnter.append("p")
                            .attr("class", "legendEntryText")
                            .text(function(d){return d.text;});
        }

        if (isArea) {
            if (!this.areas_active) {
                legendBox.append("div")
                         .attr("class", "noValues")
                         .text(this.NO_AREA_VALUES_TEXT);
            } else {
                var shades = [this.DEFAULT_COLOR];
                shades.push.apply(shades, this.CHORO_COLORS);
                makeLegend(shades, this.areas_legend_numbers);
            }
        } else { // !isArea
            if (!this.tracts_active) {
                legendBox.append("div")
                         .attr("class", "noValues")
                         .text(this.NO_TRACT_VALUES_TEXT);
            } else {
                var shades = [this.TRACT_DEFAULT_COLOR];
                shades.push.apply(shades, this.TRACT_CHORO_COLORS);
                makeLegend(shades, this.tracts_legend_numbers);
            }
        }
    },

    getCrimeNumFromID: function(id) {
        var crimeNum = 0;
        tract_arr = id.split(",");
        for (var i = 0; i < tract_arr.length; i++)
            if (this.tract_crime_numbers.hasOwnProperty(Number(tract_arr[i])))
                crimeNum += this.tract_crime_numbers[Number(tract_arr[i])];

        return crimeNum;
    },

    draw: function() {
        var width = parseInt(d3.select('#map').style('width'));
        var height = this.MAP_RATIO * width;
        console.log(height);

        var tip = d3.tip()
            .attr("class", "map-tip")
            .html(function(d) {
                var descriptorName;
                        if (d.properties.AREA_NAME) 
                            descriptorName = d.properties.AREA_NAME;
                        else
                            descriptorName = "Tract " + d.id;
                        return [descriptorName,
                                this.getCrimeNumFromID(d.id)+" Crimes"].join("<br>");
            }.bind(this));

        var svg = d3.select("#map").append("svg")
                .attr("width", width+'px')
                .attr("height", height+'px')
                .attr("id", "mapPalette")
                .append("g")
                .call(tip);
        this.svg = svg;
        d3.select("#zoomOut").on("click", this.reset.bind(this));

        var drawOverlay = function() {
            d3.json("js/apd_areas.topojson", function(error, areas_map) {
                if (error) return console.error(error);

                var areas = areas_map.objects.apd_areas;
                var geojson = topojson.feature(areas_map, areas);
                var center = d3.geo.centroid(geojson);
                var scale = 150;
                var offset = [width/2, height/2];
                var projection = d3.geo.mercator().scale(scale).center(center)
                    .translate(offset);

                var path = d3.geo.path().projection(projection);

                this.geojson = geojson;
                var bounds  = path.bounds(geojson);
                var hscale  = scale*width  / (bounds[1][0] - bounds[0][0]);
                var vscale  = scale*height / (bounds[1][1] - bounds[0][1]);
                var scale   = (hscale < vscale) ? hscale : vscale;
                var offset  = [width - (bounds[0][0] + bounds[1][0])/2,
                               height - (bounds[0][1] + bounds[1][1])/2];

                projection = d3.geo.mercator().center(center)
                    .scale(scale).translate(offset);
                path = path.projection(projection);

                

                this.svg.selectAll(".area")
                    .data(geojson.features)
                  .enter().append("path")
                    .attr("id", function(d){ return "area" + d.id; })
                    .attr("d", path)
                    .attr("class", "area")
                    .classed("clickableArea", function(d) {return d.id.split(",").length > 1})
                    .style("fill", this.DEFAULT_COLOR)
                    .style("stroke-width", "1")
                    .style("stroke", this.BORDER_COLORS)
                    .on("click", function(d) {
                        // if the area only encompasses
                        // one census tract it makes
                        // no sense at all to zoom. Same for no colors in areas.
                        
                        if(d.id.split(",").length < 2  || !this.areas_active) return; 

                        this.plotLegend(false);
                        if (this.previous_area) {
                            this.previous_area.style("visibility", "visible");
                        }

                        d3.select("#zoomOut").style("visibility", "visible");
                        // regex replace below is necessary to escape
                        // special characters present in the id
                        this.previous_area = d3.select("#area" + d.id.replace(/\./g, "\\.")
                                                                     .replace(/,/g, "\\,"))
                                               .classed("active", true)
                                               .style("visibility", "hidden");

                        // http://bl.ocks.org/mbostock/4699541
                        var bounds = this.path.bounds(d),
                            dx = bounds[1][0] - bounds[0][0],
                            dy = bounds[1][1] - bounds[0][1],
                            x = (bounds[0][0] + bounds[1][0]) / 2,
                            y = (bounds[0][1] + bounds[1][1]) / 2,
                            scale = .9 / Math.max(dx / width, dy / height),
                            translate = [width / 2 - scale * x, height / 2 - scale * y];

                        this.svg.transition()
                            .duration(750)
                            .style("stroke-width", 1.5 / scale + "px")
                            .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
                    }.bind(this))
                    .on("mouseover", tip.show)
                    .on("mouseout", tip.hide);

                // run this last, because it may be slow
                // map draw has priority. Also, this should be its
                // own function because it has little to do with drawing
                // an overlay. There should be a "setup" function calling
                // both drawOverlay and this
                var featuresArray = geojson.features;
                for (var i = 0; i < featuresArray.length; i++) {
                    var area = featuresArray[i];
                    if (area.properties.AREA_NAME) {
                        var tracts = area.id.split(',');
                        for (var j = 0; j < tracts.length; j++)
                            tracts[j] = Number(tracts[j]);
                        this.area_tracts.push(tracts);
                    }
                }
                missionControl.addClient(this.display.bind(this));
            }.bind(this));
        }.bind(this);

        d3.json("js/apd_census_tracts_pared.topojson", function(drawOverlay, error, tracts_map) {
            if (error) return console.error(error);

            var tracts = tracts_map.objects.apd_census_tracts_pared;
            var geojson = topojson.feature(tracts_map, tracts);
            var center = d3.geo.centroid(geojson);
            var scale = 150;
            var offset = [width/2, height/2];
            var projection = d3.geo.mercator().scale(scale).center(center)
                .translate(offset);

            var path = d3.geo.path().projection(projection);
            var bounds  = path.bounds(geojson);
            var hscale  = scale*width  / (bounds[1][0] - bounds[0][0]);
            var vscale  = scale*height / (bounds[1][1] - bounds[0][1]);
            var scale   = (hscale < vscale) ? hscale : vscale;
            var offset  = [width - (bounds[0][0] + bounds[1][0])/2,
                           height - (bounds[0][1] + bounds[1][1])/2];

            projection = d3.geo.mercator().center(center)
                .scale(scale).translate(offset);
            this.projection = projection;
            path = path.projection(projection);
            this.path = path;

            // svg.append("rect").attr('width', width).attr('height', height)
            //         .style('stroke', 'black').style('fill', 'none');

            svg.selectAll(".tract")
                    .data(geojson.features)
                  .enter().append("path")
                    .attr("id", function(d){ return "tract" + d.id; })
                    .attr("class", "tract")
                    .attr("d", path)
                    .style("fill", this.TRACT_DEFAULT_COLOR)
                    .style("stroke-width", "1")
                    .style("stroke", this.BORDER_COLORS)
                    .on("mouseover", tip.show)
                    .on("mouseout", tip.hide);
            drawOverlay();
        }.bind(this, drawOverlay));
    },
    display: function(start, end, catNum) {
        this.reset();
        reqMaker.district_count(start, end, null, catNum, function(err, resp) {
            var data = {};
            for (var i = 0; i < resp.length; i++)
                data[Number(resp[i]['offense_census_tract'])] = resp[i]['count'];
            this.color(data);
            this.plotLegend(true);

        }.bind(this));
    },
    color: function(data) { // spaghetti code at this point, needs a refactor
        this.tract_crime_numbers = {};
        for (tract_num in data)
            if (data.hasOwnProperty(tract_num))
                this.tract_crime_numbers[Number(tract_num)] = Number(data[tract_num])
        var number_of_shades = this.CHORO_COLORS.length;
        var area_shades = [this.DEFAULT_COLOR];
        area_shades.push.apply(area_shades, this.CHORO_COLORS);
        var tract_shades = [this.TRACT_DEFAULT_COLOR];
        tract_shades.push.apply(tract_shades, this.TRACT_CHORO_COLORS);

        var maxNumCrimesTracts = 0;

        for (tract in data)
            if (data.hasOwnProperty(tract))
                if (data[tract] > maxNumCrimesTracts) maxNumCrimesTracts = data[tract];

        var maxNumCrimesAreas = maxNumCrimesTracts;

        for (var i = 0; i < this.area_tracts.length; i++) {
            var area_tract = this.area_tracts[i];
            var numCrimesInArea = 0;
            for (var j = 0; j < area_tract.length; j++) {
                numCrimesInArea += data[area_tract[j]];
            }
            if (numCrimesInArea > maxNumCrimesAreas) 
                maxNumCrimesAreas = numCrimesInArea;
        }

        if (maxNumCrimesAreas < number_of_shades) { // we have too few crimes to 
                this.svg.selectAll(".area")    // fill the map
                .style("fill", function(d) {
                    return this.DEFAULT_COLOR;
                }.bind(this));
                this.areas_active = false;
                return;
        }
        this.areas_active = true;

        // crimeNumbers is a list of NUMBER_OF_SHADES values to be
        // used to map numbers of crimes to colors on the map.
        // so if maxNumCrimes is 10 and NUMBER_OF_SHADES is 5, 
        // then crimeNumbers is [1, maxNumCrimes*1/NUMBER_OF_SHADES,
        //                       maxNumCrimes*2/NUMBER_OF_SHADES,
        //                       ..., maxNumCrimes*(NUMBER_OF_SHADES-1)/NUMBER_OF_SHADES]
        //                      = [1, 2, 4, 6, 8]
        // and these values map to the following colors for 
        // each tract, area, etc.:
        // (-inf, 1): this.DEFAULT_COLOR (think of as color 0)
        // [1, 2):    color1
        // [2, 4):    color2
        // [4, 6):    color3
        // [6, 8):    color4
        // [8, +inf): color5
        // the behavior will hold for combinations of values
        // that produce floats, but for the purposes of displaying
        // a legend it's recommended that you round up the values
        // on the legend to whole numbers.
        // I would change that detail here but I eventually may
        // want this to work for percentages (e.g. crimes/resident)
        // and that would make the task of changing this code harder

        var selectFill = function(d) {
            var numCrimes = 0;
            var idsToLookup = d.id.split(',');
            
            for (var i = 0; i < idsToLookup.length; i++) {
                var idToLookup = Number(idsToLookup[i]);
                numCrimes += (this.data.hasOwnProperty(idToLookup)) ? this.data[idToLookup] : 0;
            }
            return this.color(numCrimes);
        };

        var crimeNumbersAreas = [1];

        for (var i = 1; i < number_of_shades; i++)
            crimeNumbersAreas.push(maxNumCrimesAreas*i/number_of_shades);

        this.areas_legend_numbers = crimeNumbersAreas.slice(1);
        this.areas_legend_numbers.push(maxNumCrimesAreas);


        var colorAreas = d3.scale.threshold()
            .domain(crimeNumbersAreas)
            .range(area_shades);

        this.svg.selectAll(".area")
        .style("fill", selectFill.bind({color:colorAreas,
                                        data:data}));

        if (maxNumCrimesTracts < number_of_shades) { // we have too few crimes for the tract level view
            this.svg.selectAll(".tract")
            .style("fill", function(d) {
                this.TRACT_DEFAULT_COLOR;
            }.bind(this));
            this.tracts_active = false;
        } else {
            this.tracts_active = true;
            var crimeNumbersTracts = [1];

            for (var i = 1; i < number_of_shades; i++)
                crimeNumbersTracts.push(maxNumCrimesTracts*i/number_of_shades);

            this.tracts_legend_numbers = crimeNumbersTracts.slice(1);
            this.tracts_legend_numbers.push(maxNumCrimesTracts);

            var colorTracts = d3.scale.threshold()
            .domain(crimeNumbersTracts)
            .range(tract_shades);

            this.svg.selectAll(".tract")
            .style("fill", selectFill.bind({color:colorTracts,
                                            data:data}));
        }        

    },
    reset: function() {
        d3.select("#zoomOut").style("visibility", "hidden");
        d3.selectAll(".area").style("visibility", "visible");
        this.plotLegend(true);
        this.svg.transition()
        .duration(750)
        .style("stroke-width", "1.5px")
        .attr("transform", "");
    },
    resize: function() {
        var scale = 150;
        var width = parseInt(d3.select('#map').style('width'));
        var height = width * this.MAP_RATIO;

        var center = d3.geo.centroid(this.geojson);
        var scale = 150;
        var offset = [width/2, height/2];
        var projection = d3.geo.mercator().scale(scale).center(center)
            .translate(offset);

        var path = d3.geo.path().projection(projection);
        var bounds  = path.bounds(this.geojson);
        var hscale  = scale*width  / (bounds[1][0] - bounds[0][0]);
        var vscale  = scale*height / (bounds[1][1] - bounds[0][1]);
        var scale   = (hscale < vscale) ? hscale : vscale;
        var offset  = [width - (bounds[0][0] + bounds[1][0])/2,
                       height - (bounds[0][1] + bounds[1][1])/2];
        this.projection
            .translate(offset)
            .scale(scale);

        this.path = path.projection(this.projection);

        d3.select("#mapPalette")
            .attr("width", width+'px')
            .attr("height", height+'px')

        this.svg.selectAll('.area').attr('d', this.path);
        this.svg.selectAll('.tract').attr('d', this.path);

    }
}

$().ready(function () {
    var crimeMap = Object.create(CrimeMap);
    crimeMap.draw.bind(crimeMap)();
    d3.select(window).on('resize', crimeMap.resize.bind(crimeMap));
});
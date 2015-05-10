var InteractiveController = {
    MILLISECONDS_IN_A_DAY:  24 * 60 * 60 * 1000,
    DAYS_IN_THE_PAST: 500,
    DAYS_IN_PAST_FOR_DEFAULT: 7,
    MAX_RANGE: 30,
    MIN_RANGE: 2,
    DAYS_FROM_PRESENT: 7,
    slider: null,
    clients: [],

    setup: function() {
        // this.slider = $("#slider");
        var MILLISECONDS_IN_THE_PAST = this.DAYS_IN_THE_PAST * this.MILLISECONDS_IN_A_DAY;
        var MILLISECONDS_IN_THE_PAST_DEFAULT = this.DAYS_IN_PAST_FOR_DEFAULT * this.MILLISECONDS_IN_A_DAY;
        // var MONTHS = ["Jan.", "Feb.", "March", "April",
        //               "May", "June", "July", "Aug.", "Sep.",
        //               "Oct.", "Nov.", "Dec."];
        // this.slider.dateRangeSlider(
        //     {
        //         bounds: { // future improvement: account for timezone in setting bounds
        //             min:  new Date(Date.now() - MILLISECONDS_IN_THE_PAST),
        //             max: new Date()
        //         },
        //         defaultValues: {
        //             min: new Date(Date.now() - MILLISECONDS_IN_THE_PAST_DEFAULT),
        //             max: new Date()
        //         },
        //         step: {
        //             days:1
        //         },
        //         range: {
        //             min: {days: 2},
        //             max: {days: 30}
        //         },
        //         formatter: function(val) {
        //             var day = val.getDate(),
        //                 month = val.getMonth(),
        //                 year = val.getFullYear();
        //             return MONTHS[month] + " " + day + ", " + year;
        //         },
        //         scales: [{
        //             next: function(value) {
        //                 var next = new Date(value);
        //                 return new Date(next.setMonth(value.getMonth() + 1));
        //             },
        //             label: function(value) {
        //                 return MONTHS[value.getMonth()] + " " 
        //                 + value.getFullYear().toString().slice(-2);
        //             }
        //         }]
        //     }
        // );
        // $("#updateButton").click(this.update.bind(this));

        $('#slider span').html(moment().subtract(this.DAYS_FROM_PRESENT + this.DAYS_IN_PAST_FOR_DEFAULT, 'days').format('MMMM D, YYYY') + ' - ' + moment().subtract(this.DAYS_FROM_PRESENT, 'days').format('MMMM D, YYYY'));
        this.slider = $("#slider").daterangepicker({
            minDate: moment().subtract(this.DAYS_IN_THE_PAST, 'days'),
            maxDate: moment().subtract(this.DAYS_FROM_PRESENT, 'days'),
            startDate: moment().subtract(this.DAYS_FROM_PRESENT + this.DAYS_IN_PAST_FOR_DEFAULT, 'days'),
            endDate: moment().subtract(this.DAYS_FROM_PRESENT, 'days'),
            timePicker: false,
            dateLimit: {days: this.MAX_RANGE},
            showDropdowns: true,
            opens: 'right',
            ranges: {
               'Last Week': [moment().subtract('days', 13), moment().subtract('days', 7)],
               'Last 30 Days': [moment().subtract('days', 36), moment().subtract('days', 7)],
               'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
            },
        },
        function(start, end, label) {
            console.log(start.toISOString(), end.toISOString(), label);
            $('#slider span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        );

        this.slider.on("apply.daterangepicker", function(ev, picker) {
            this.update();
        }.bind(this));

        var catClick = function(event) {
                         $(".catSelectorItem").removeClass("active");
                         $(this).parent().addClass("active");
                         $("#categorySelectorButton")
                         .text($('.catSelectorItem.active a').text())
                            .append(' <span class="caret"></span>');
                         missionControl.update(); // keep the page from jumping up
                       };
        $("#categorySelectorButton").text("All Crimes")
            .append(' <span class="caret"></span>');
        var catSelector = $("#categorySelector");
        var catItem = $('<li>', {'class': 'catSelectorItem active'})
                            .append($('<a>', { 'href': '#',
                                                on: {
                                                  click: catClick
                                                }
                                              }).text("All Crimes").data('catID', null));
        console.log(catItem);
        catSelector.append(catItem);
        reqMaker.category_list(function (catClick, err, resp) {
            for (var i = 0; i < resp.length; i++) {
                catItem = $('<li>', {'class': 'catSelectorItem'})
                            .append($('<a>', { 'href': '#',
                                                on: {
                                                  click: catClick
                                                }
                                              }).text(resp[i]['name']).data('catID', resp[i]['id']));
                this.append(catItem);
            }
        }.bind(catSelector, catClick));
    },

    addClient: function(clientFunction) {
        this.clients.push(clientFunction);
    },

    update: function() {
        console.log(this.slider.data('daterangepicker').startDate.toDate());
        console.log(this.slider.data('daterangepicker').endDate.toDate());
        
        for (var i = 0; i < this.clients.length; i++)
            this.clients[i](this.slider.data('daterangepicker').startDate.toDate(), 
                            this.slider.data('daterangepicker').endDate.toDate(), 
                            $('.catSelectorItem.active a').data('catID'));
    }

};
var missionControl;

$().ready(function () {
    missionControl = Object.create(InteractiveController);
    missionControl.setup(); 
});
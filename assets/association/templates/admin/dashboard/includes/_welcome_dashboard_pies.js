{% load i18n %}
{% load assets_tags %}


$('#dash_pie_earnings').highcharts({
    chart: {
        //type: 'area'
        polar: true,
        type: 'column',
    },
    title: {
        text: '{% trans "Earnings" %}'
    },

	    pane: {
            size: '85%'
	    },
		legend: {
			reversed: true,
			align: 'right',
			verticalAlign: 'top',
			y: 100,
			layout: 'vertical'
		},
			    
    xAxis: {
        categories: [{% for m in month_names %} '{{m}}', {% endfor %}],
        //tickmarkPlacement: 'on',
        //title: { enabled: false }
    },
    yAxis: {
        //title: { text: '{% trans "Amount" %}' },
        min: 0,
		endOnTick: false,
		showLastLabel: true,
    },
    tooltip: {
        shared: true,
        valueSuffix: ' €'
    },
    plotOptions: {
        series: {
            stacking: 'normal',
			shadow: false,
        },
	    column: {
	        pointPadding: 0,
	        groupPadding: 0
	    }
    },
    series: [
{% for key, values in results_earnings.items %}
    {
        name: '{{key}}',
        data: [ {% for res in values %} {{ res.amount_earning|amount }}, {% endfor %} ],
        color: colors_earning[ {{ forloop.counter }} ]
    },
{% endfor %}
    ]
});

// SPENDINGS ------------------------------------------------------------------

$('#dash_pie_spendings').highcharts({
    chart: {
        //type: 'area'
        polar: true,
        type: 'column'
    },
    title: {
        text: '{% trans "Spendings" %}'
    },

	    pane: {
            size: '85%'
	    },
		legend: {
			reversed: true,
			align: 'right',
			verticalAlign: 'top',
			y: 100,
			layout: 'vertical'
		},
			    
    xAxis: {
        categories: [{% for m in month_names %} '{{m}}', {% endfor %}],
        //tickmarkPlacement: 'on',
        //title: { enabled: false }
    },
    yAxis: {
        //title: { text: '{% trans "Amount" %}' },
        min: 0,
		endOnTick: false,
		showLastLabel: true,
    },
    tooltip: {
        shared: true,
        valueSuffix: ' €'
    },
    plotOptions: {
        series: {
            stacking: 'normal',
			shadow: false,
        },
	    column: {
	        pointPadding: 0,
	        groupPadding: 0
	    }
    },
    series: [
{% for key, values in results_spendings.items %}
    {
        name: '{{key}}',
        data: [ {% for res in values %} {{ res.amount_spending|amount }}, {% endfor %} ],
        color: colors_spending[ {{ forloop.counter }} ]
    },
{% endfor %}
    ]
});

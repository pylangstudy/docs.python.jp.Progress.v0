window.onload = function(){
    Main();
}
function Main()
{
//    var tsvUrl = "https://raw.githubusercontent.com/pylangstudy/201705/master/25/01/pylangstudy.HeadingToAggregate.201705252124/contents.tsv"
    var tsvUrl = "./contents.tsv"
    d3.tsv(tsvUrl, function(error, data) {
        var total = data.length;
        var counts = GetAggregateCounts(data);
        console.log(counts);
        d3.select('body').append(function(){return CreateProgressRateTable(counts);});
        d3.select('body').append(function(){return CreateStatusTable(counts);});
        d3.select('body').append(function(){return CreateHeadingTable(data);});
    });
}

function CreateProgressRateTable(counts) {
    var table = document.createElement('table');
    d3.select(table).attr('id', 'ProgressRate');
    var tr = document.createElement('tr');
    d3.select(tr).append('th').text('進捗率');
    d3.select(tr).append('td').text("" + counts.progressRate + ' % (' + (counts.finished + counts.zeroFinished) + '/' + counts.total + ')');            
    d3.select(table).append(function(){return tr;});
    return table;
}

function CreateStatusTable(counts) {
    var table = document.createElement('table');
    d3.select(table).attr('id', 'Status');
    var thead = document.createElement('thead');
    var tbody = document.createElement('tbody');
    var tr = document.createElement('tr');
    
    d3.select(tr).append('th').append('img').attr('src', GetFaviconApiUrl('github.com')).attr('title', '完了 成果物あり');
    AppendStatusTd(tr, counts.finished, counts.total, '完了 成果物あり', 'Finished');
    
    d3.select(tr).append('th').attr('title', '完了 成果物なし').text('-');
    AppendStatusTd(tr, counts.zeroFinished, counts.total, '完了 成果物なし', 'ZeroFinished');
    
    d3.select(tr).append('th').attr('title', '未完了').text('未');
    AppendStatusTd(tr, counts.unfinished, counts.total, '未完了', 'Unfinished');
    
    d3.select(tbody).append(function(){return tr;});
    d3.select(table).append(function(){return thead;});
    d3.select(table).append(function(){return tbody;});
    return table;
}

function AppendStatusTd(tr, value, total, title, class_) {
    td = document.createElement('td');
    d3.select(td).append(function(){return GetStatusTdCount(value, title);});
    d3.select(td).append(function(){return GetStatusTdProgressRate(value, total, title);});
    d3.select(td).attr('class', class_);
    d3.select(tr).append(function(){return td;});
}

function GetStatusTdCount(value, title) {
    span = document.createElement('span');
    d3.select(span).attr('title', title).text(value);
    return span;
}
function GetStatusTdProgressRate(value, total, title) {
    small = document.createElement('small');
    d3.select(small).attr('title', title).text('(' + (value / total).toFixed(4) + '%)');
    return small;
}

function GetStatusTdText(value, total) {
    return value + ' (' + (value / total).toFixed(4) + '%)';
}

function GetAggregateTableHeader(tbody, counts) {
    tr1 = tbody.append('tr');
    tr1.append('th').text('進捗率');
    tr1.append('td').text("" + counts.progressRate + ' % (' + (counts.finished + counts.zeroFinished) + '/' + counts.total + ')');
    tr2 = tbody.append('tr');
    tr2.append('th').append('img').attr('src', GetFaviconApiUrl('github.com')).attr('title', '完了 成果物あり');
    tr2.append('td').text(counts.finished);
    tr3 = tbody.append('tr');
    tr3.append('th').attr('title', '完了 成果物なし').text('-');
    tr3.append('td').text(counts.zeroFinished);
    tr4 = tbody.append('tr');
    tr4.append('th').attr('title', '未完了').text('未');
    tr4.append('td').text(counts.unfinished);
}

function GetFaviconApiUrl(domain) {
    return "http://www.google.com/s2/favicons?domain=" + domain;
}

function GetAggregateCounts(data) {
    counts = {'total': 0, 'finished': 0, 'zeroFinished': 0, 'unfinished': 0, 'progressRate': 0};
    counts['total'] = data.length;
    for (var i = 0; i < data.length; i++) {
        if (!data[i].hasOwnProperty('GitHubUrl')) {console.log('bbbbb');continue;}
        else if ('' == data[i]['GitHubUrl']) { counts['unfinished']++; }
        else if ('-' == data[i]['GitHubUrl']) { counts['zeroFinished']++; }
        else if (data[i]['GitHubUrl'].startsWith('http://')
              || data[i]['GitHubUrl'].startsWith('https://')) {
            counts['finished']++;
        }
        else {throw new Error("'tsvの3列目には空値,-,URLのどれかを記入してください。: " + data['GitHubUrl']);}
    }
    counts['progressRate'] = ((counts['finished'] + counts['zeroFinished']) / counts['total']) * 100;
    return counts;
}

function CreateHeadingTable(data) {
    var table = document.createElement('table');
    d3.select(table).attr('id', 'List');
    var thead = document.createElement('thead');
    var tbody = document.createElement('tbody');

    // ヘッダ
    var headerKyes = d3.map(data[0]).keys(); //ヘッダー用にkeyを取得
    d3.select(thead).append('tr')
        .selectAll('th')
        .data(GetHeader())
        .enter()
        .append(function(d){return d;});
    // データ
    d3.select(tbody).selectAll('tr')
        .data(data)
        .enter()
        .append(function(row) { return GetTr(row); })
            .selectAll('td')
            .data(function (row) { 
                return GetRowData(row);
            }) 
            .enter()
            .append('td')
            .append(function(d) { return GetTd(d); })

    d3.select(table).append(function(){return thead;});
    d3.select(table).append(function(){return tbody;});
    return table;
}

function GetTr(row) {
    tr = document.createElement('tr');
    if (!row.hasOwnProperty('GitHubUrl')) {return tr;}
    else if ('' == row['GitHubUrl']) { d3.select(tr).attr('class', "Unfinished"); }
    else if ('-' == row['GitHubUrl']) { d3.select(tr).attr('class', "ZeroFinished"); }
    else if (row['GitHubUrl'].startsWith('http://')
          || row['GitHubUrl'].startsWith('https://')) {
        d3.select(tr).attr('class', "Finished");
    }
    else {throw new Error("'tsvの3列目には空値,-,URLのどれかを記入してください。: " + row['GitHubUrl']);}
    return tr;
}

function GetHeader() {
    th1 = document.createElement('th');
    d3.select(th1).attr('title', '成果物');
    d3.select(th1).text('果');
    th2 = document.createElement('th');
    d3.select(th2).text('参照元');
    return [th1, th2];
}

function GetRowData(row) {
    return [
        {'GitHubUrl': row['GitHubUrl']},
        {'DocumentUrl': row['DocumentUrl'], 'Title': row['Title']}
    ];
}

function GetTd(data) {
    if (data.hasOwnProperty('GitHubUrl')) {
        return GetArtifactsHtml(data);
    } else {
        return GetReferenceHtml(data);
    }
}
function GetArtifactsHtml(data) {
    if (undefined == data['GitHubUrl']) { console.log(data); return; } // どこかで undefined になっている。詳細不明。
    if ('' == data['GitHubUrl']) {
        span = document.createElement('span');
        d3.select(span).text('未');
        return span;
    } else if ('-' == data['GitHubUrl']) {
        span = document.createElement('span');
        d3.select(span).text('-');
        return span;
    } else if (data['GitHubUrl'].startsWith('http://')
            || data['GitHubUrl'].startsWith('https://')) {
        a = document.createElement('a');
        d3.select(a).attr('href', data['GitHubUrl']);
        dirs = data['GitHubUrl'].split('/');
        d3.select(a).attr('title', dirs[dirs.length-1]);
        d3.select(a).append('img').attr('src', GetFaviconApiUrl(data['GitHubUrl'].split('/')[2]));
        return a;
    } else {
        throw new Error("'tsvの3列目には空値,-,URLのどれかを記入してください。: " + data['GitHubUrl']);
    }
}
function GetReferenceHtml(data) {
    a = document.createElement('a');
    d3.select(a).attr('href', "https://docs.python.jp/3/" + data['DocumentUrl'])
    d3.select(a).text(data['Title'])
    return a
}

/**
 # -*- encoding: utf-8 -*-
 # ===================================================
 # phone:10086
 # email: tangdayi520@126.com
 # projectname: FBBFoods
 # file_name: productAPI
 # author: tangdayi
 # data: 2018年05月24日 21时05分
 # ===================================================
 */

/*********************************************************************************************************************************
 *
 * Ajax 请求数据接口， 提供的函数进行动态更新
 * 接口调用完毕后间隔 1 s 继续调用本函数，以达到实时请求数据，实时更新的效果
 *
 *********************************************************************************************************************************/



/***
 *
 * 切入html片段
 * 获取 product html
 * @returns {Array}
 */

function getPtoHtml() {
    var allProducts = requestAllProducts();
    var htmlPro =[]
    for (var i=0; i<=allProducts.length-50; i++){
        var obj = allProducts[i];
        var o = obj['name'];
        htmlPro.push('<div class="am-u-sm-3 am-u-md-2 text-three last big">');
        htmlPro.push('<div class="outer-con ">');
        htmlPro.push('<div class="title">'+allProducts[i]['name']+'</div>');
        htmlPro.push('<div class="sub-title">'+allProducts[i]['list_price']+'</div>');
        htmlPro.push('<i class="am-icon-shopping-basket am-icon-md seprate"></i></div>');
        htmlPro.push('<a href="#"><img src="/web/image?model=product.template&field=image_medium&id='+allProducts[i]["id"]+'"/>');
        htmlPro.push('</a></div>');
    }
    // /web/image?model=product.template&field=image_medium&id=
    // /web/image/product.template/18/image
    // 将数组转成字符串
    htmlPro = htmlPro.join('')
    return htmlPro
}

/**
 * 后台数据请求
 * @returns {Array}
 */
function requestAllProducts() {
    var jsonData = []
    $.ajax({
        type: 'post',
        async:false,  // 现获取数据在加载html，获取到数据才加载html
        url: '/fbb/product/list',  // 获取数据列表链接
        success: function(data) {
            data = JSON.parse(data);
            jsonData = data['data']
        },
        cache: false
      });
    return jsonData;
}


/***
 *
 * 产品接口调用
 * 通过公司Id
 * @param company_id
 */
function requestProductAPICompanyId(company_id) {
    var jsonData = []
    $.ajax({
        type: 'post',
        async:false,  // 现获取数据在加载html，获取到数据才加载html
        url: '/fbb/product/list?company_id='+company_id,   // 获取数据列表链接
        success: function(data) {
            data = JSON.parse(data);
            jsonData = data['data']
        },
        cache: false
      });
    return jsonData;
}

/**
 * 通过产品ID
 * @param product_id
 */
function requestProductAPIPid(product_id) {

}

/***
 * 通过产品ID和公司ID
 * @param product_id
 * @param company_id
 */
function requestProductAPIPidCid(product_id,company_id) {

}



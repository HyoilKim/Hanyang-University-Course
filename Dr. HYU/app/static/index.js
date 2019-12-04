$(document).ready(() => {
  var container = $("#map").get(0)
      var options = { 
        center: new kakao.maps.LatLng(37.5585146, 127.0331892), 
        level: 4
      };
      var map = new kakao.maps.Map(container, options);

      // 마커 표시
      var marker = new kakao.maps.Marker({ 
          position: map.getCenter() 
      }); 
      marker.setMap(map);

      // 마우스 드래그로 지도 이동이 완료되었을 때 마지막 파라미터로 넘어온 함수를 호출하도록 이벤트를 등록합니다
      kakao.maps.event.addListener(map, 'dragend', function() {          
        var latlng = map.getCenter(); 
      });


      // 마커에 나타낼 내용(병원, 상점 정보들)
      var iwContent = '<div style="padding:5px;">Hello World!</div>'; 
      var infowindow = new kakao.maps.InfoWindow({
          content : iwContent
      });
      kakao.maps.event.addListener(marker, 'mouseover', function() {
          infowindow.open(map, marker);
      });
      kakao.maps.event.addListener(marker, 'mouseout', function() {
          infowindow.close();
      });

      // 마커에 클릭이벤트를 등록합니다
      kakao.maps.event.addListener(marker, 'click', function() {
        // 자주가는 병원등록 하기
        // 예약하기
        // 처방전 확인
      });
})

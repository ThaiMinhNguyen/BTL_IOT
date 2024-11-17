import { Row, Col } from 'antd';
import React from 'react';
import ProfileCard from "./ProfileCard";
import "./Profiles.scss";

function Profiles() {
  const profiles = [
    {
      id: 1,
      name: "Lê Đoàn Ngọc Nam",
      className: "D21HTTT3",
      studentId: "B21DCCN546",
      avatarUrl: "https://scontent.fhan7-1.fna.fbcdn.net/v/t39.30808-6/440780299_1509728313003877_8090341391507448441_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeFoohLhTCkpW1kKeQItvRft2PSYGFSB-oTY9JgYVIH6hAJ3qT4oAcvAb-I4XTAImjyRCzNdrznWYqxrBa5GVnKy&_nc_ohc=F4e3hThIxdYQ7kNvgE98NRw&_nc_ht=scontent.fhan7-1.fna&_nc_gid=AuJNZAvveHFutENoVHay0gy&oh=00_AYAZjqAbsANT90n-wvWeYhro_3l3XtVnmHPTfqP3JmqUoQ&oe=6700AA30",
      coverUrl: "https://baobinhdinh.vn/viewimage.aspx?imgid=141133",
    },
    {
      id: 2,
      name: "Lừ Thị Thưởng",
      className: "D21CNPM1",
      studentId: "B21DCCN701",
      avatarUrl: "https://scontent.fhan18-1.fna.fbcdn.net/v/t39.30808-6/404468562_1360735678150906_2227544323508199255_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeEEGKD7GtI4tObz6KOiQQnDciJV2oCqxvRyIlXagKrG9MJ4ANac2yX_G1ggidKlHZsFaXSZMXiuOVCJKW_5u9CU&_nc_ohc=7c-AfTl1ytwQ7kNvgGH9SUl&_nc_ht=scontent.fhan18-1.fna&_nc_gid=ATsWdVKCw2toFKzRG4z7Z-O&oh=00_AYA4QhMyxEa3Ixg6VYDDfkK7Kv3GfBvfiB3LcwFfSRoXmQ&oe=66D0CEB9",
      coverUrl: "https://www.baokontum.com.vn/uploads/Image/2023/05/07/173837pasted%20image%200.png",
    },
    {
      id: 3,
      name: "Nguyễn Thái Minh",
      className: "D21CNPM3",
      studentId: "B21DCCN090",
      avatarUrl: "https://scontent.fsgn14-1.fna.fbcdn.net/v/t39.30808-6/383389461_1030759194612783_7210132979547887269_n.jpg?stp=cp6_dst-jpg_s720x720&_nc_cat=104&ccb=1-7&_nc_sid=833d8c&_nc_eui2=AeEB9cnuAMEmHfZ7bCgN87rSvndslI9rG-S-d2yUj2sb5HWdXDhmrXBumSBRTv0w1W1-udH2K8VgtrJJ8H7FzWgP&_nc_ohc=9ru2FWqPnKkQ7kNvgFxnTcB&_nc_ht=scontent.fsgn14-1.fna&oh=00_AYDPSTKZPw9zvqqEAzog4M0vh4a_WugceQwQMo2uiO9BVg&oe=66D1D1AA",
      coverUrl: "https://gcs.tripi.vn/public-tripi/tripi-feed/img/473615Pmt/image-200-anh-hoang-hon-dep-buon-co-don-lang-man-cuc-chill-167642975045324.jpg",
    },
    {
      id: 4,
      name: "Nguyễn Tiến Thắng",
      className: "D21CNPM6",
      studentId: "B21DCCN670",
      avatarUrl: "https://scontent.fsgn14-1.fna.fbcdn.net/v/t39.30808-6/383389461_1030759194612783_7210132979547887269_n.jpg?stp=cp6_dst-jpg_s720x720&_nc_cat=104&ccb=1-7&_nc_sid=833d8c&_nc_eui2=AeEB9cnuAMEmHfZ7bCgN87rSvndslI9rG-S-d2yUj2sb5HWdXDhmrXBumSBRTv0w1W1-udH2K8VgtrJJ8H7FzWgP&_nc_ohc=9ru2FWqPnKkQ7kNvgFxnTcB&_nc_ht=scontent.fsgn14-1.fna&oh=00_AYDPSTKZPw9zvqqEAzog4M0vh4a_WugceQwQMo2uiO9BVg&oe=66D1D1AA",
      coverUrl: "https://cdn.mobilecity.vn/mobilecity-vn/images/2024/05/hinh-nen-bau-troi-1.jpg.webp",
    },
  ];

  return (
    <div className="profiles-container">
      <Row gutter={16}>
        {profiles.map(profile => (
          <Col span={6} key={profile.id}>
            <ProfileCard
              name={profile.name}
              className={profile.className}
              studentId={profile.studentId}
              avatarUrl={profile.avatarUrl}
              coverUrl={profile.coverUrl}
            />
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default Profiles;

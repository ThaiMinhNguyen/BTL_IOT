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
      avatarUrl: "https://tingenz.com/wp-content/uploads/2022/12/de-thuong-gau-chibi-cute-min.jpg",
      coverUrl: "https://baobinhdinh.vn/viewimage.aspx?imgid=141133",
    },
    {
      id: 2,
      name: "Lừ Thị Thưởng",
      className: "D21CNPM1",
      studentId: "B21DCCN701",
      avatarUrl: "https://phunugioi.com/wp-content/uploads/2020/02/hinh-anh-cute-564x362.jpg",
      coverUrl: "https://img.thuthuatphanmem.vn/uploads/2018/10/08/anh-phong-canh-nui-non-dep_093817809.jpg",
    },
    {
      id: 3,
      name: "Nguyễn Thái Minh",
      className: "D21CNPM3",
      studentId: "B21DCCN090",
      avatarUrl: "https://toigingiuvedep.vn/wp-content/uploads/2021/06/hinh-anh-hoat-hinh-de-thuong-cute-lam-avatar.jpg",
      coverUrl: "https://gcs.tripi.vn/public-tripi/tripi-feed/img/473615Pmt/image-200-anh-hoang-hon-dep-buon-co-don-lang-man-cuc-chill-167642975045324.jpg",
    },
    {
      id: 4,
      name: "Nguyễn Tiến Thắng",
      className: "D21CNPM6",
      studentId: "B21DCCN670",
      avatarUrl: "https://w0.peakpx.com/wallpaper/622/678/HD-wallpaper-sung-jin-woo-art-manhwa-anime.jpg",
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

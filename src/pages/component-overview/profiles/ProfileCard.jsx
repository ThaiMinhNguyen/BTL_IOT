import React from "react";
import "./ProfileCard.scss";
import { Card } from "antd";
import { GithubOutlined } from '@ant-design/icons';

function ProfileCard({ name, className, studentId, avatarUrl, coverUrl, githubUrl }) {
  return (
    <Card
      cover={<img alt="cover" src={coverUrl} className="cover-image" />}
      className="profile-card"
    >
      <div className="avatar">
        <img src={avatarUrl} alt="avatar" />
      </div>
      <div className="info">
        <h2>{name}</h2>
        <p>Lớp: {className}</p>
        <p>Mã sinh viên: {studentId}</p>
      </div>
    </Card>
  );
}

export default ProfileCard;

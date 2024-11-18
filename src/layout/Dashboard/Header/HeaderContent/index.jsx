import React, { useState, useEffect } from 'react';
import useMediaQuery from '@mui/material/useMediaQuery';
import IconButton from '@mui/material/IconButton';
import { Link, useLocation } from 'react-router-dom';
import Search from './Search';
import { TeamOutlined } from '@ant-design/icons';

// ==============================|| HEADER - CONTENT ||============================== //

export default function HeaderContent() {
  const downLG = useMediaQuery((theme) => theme.breakpoints.down('lg'));
  const [isProfileActive, setIsProfileActive] = useState(false);
  const location = useLocation();

  // Kiểm tra xem hiện tại có ở trang Profiles hay không
  useEffect(() => {
    if (location.pathname === '/profiles') {
      setIsProfileActive(true);
    } else {
      setIsProfileActive(false);
    }
  }, [location.pathname]);

  return (
    <>
      {!downLG && <Search />}
      <IconButton
        component={Link}
        to="/profiles"
        color="secondary"
        title="View Profiles"
        sx={{
          color: 'text.primary',
          backgroundColor: isProfileActive ? '#e6f7ff' : 'transparent', // Giữ sáng nếu đang xem profile
          transition: 'background-color 0.3s, transform 0.3s',
          '&:hover': {
            backgroundColor: '#e6f7ff',
            transform: 'scale(1.1)',
          },
        }}
      >
        <TeamOutlined />
      </IconButton>
    </>
  );
}

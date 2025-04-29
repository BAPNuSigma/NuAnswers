import React from 'react';
import { Container, Typography, Paper, Box, Link } from '@mui/material';

const Contact = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Contact Us
        </Typography>
        
        <Typography variant="body1" paragraph>
          We're here to help! If you have any questions, concerns, or feedback about NuAnswers, please don't hesitate to reach out.
        </Typography>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            General Inquiries
          </Typography>
          <Typography variant="body1" paragraph>
            Email: support@nuanswers.org
          </Typography>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Technical Support
          </Typography>
          <Typography variant="body1" paragraph>
            For technical issues or bug reports, please email: tech@nuanswers.org
          </Typography>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Legal
          </Typography>
          <Typography variant="body1">
            Please review our{' '}
            <Link href="/legal/privacy-policy">Privacy Policy</Link>
            {' '}and{' '}
            <Link href="/legal/terms-of-service">Terms of Service</Link>
            {' '}for more information about your rights and our obligations.
          </Typography>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Response Time
          </Typography>
          <Typography variant="body1" paragraph>
            We strive to respond to all inquiries within 24-48 hours during business days.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Contact; 
import React from 'react';
import { Box, Container, Typography, Paper } from '@mui/material';

const PrivacyPolicy = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Privacy Policy
        </Typography>
        <Typography variant="body1" paragraph>
          Last updated: {new Date().toLocaleDateString()}
        </Typography>
        
        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          1. Information We Collect
        </Typography>
        <Typography variant="body1" paragraph>
          We collect information that you provide directly to us when using our tutoring services, including:
          - Questions and conversations with our AI tutor
          - Basic usage data to improve our service
          - Optional feedback you provide
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          2. How We Use Your Information
        </Typography>
        <Typography variant="body1" paragraph>
          We use the information we collect to:
          - Provide and improve our tutoring services
          - Analyze and enhance the effectiveness of our AI responses
          - Maintain and optimize our platform
          - Protect against misuse of our services
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          3. Data Security
        </Typography>
        <Typography variant="body1" paragraph>
          We implement appropriate technical and organizational measures to protect your information against unauthorized access, alteration, disclosure, or destruction.
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          4. Contact Information
        </Typography>
        <Typography variant="body1" paragraph>
          For any questions about this Privacy Policy, please contact us at:
          support@nuanswers.org
        </Typography>

        <Typography variant="body2" sx={{ mt: 4, color: 'text.secondary' }}>
          This privacy policy is intended to help you understand how we handle your information and to comply with applicable privacy laws and regulations.
        </Typography>
      </Paper>
    </Container>
  );
};

export default PrivacyPolicy; 
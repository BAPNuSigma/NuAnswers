import React from 'react';
import { Container, Typography, Paper } from '@mui/material';

const TermsOfService = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Terms of Service
        </Typography>
        <Typography variant="body1" paragraph>
          Last updated: {new Date().toLocaleDateString()}
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          1. Acceptance of Terms
        </Typography>
        <Typography variant="body1" paragraph>
          By accessing and using NuAnswers, you agree to be bound by these Terms of Service and all applicable laws and regulations.
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          2. Service Description
        </Typography>
        <Typography variant="body1" paragraph>
          NuAnswers provides an AI-powered tutoring service designed to assist students with their academic questions. The service is provided "as is" and we make no warranties about the accuracy or completeness of any information provided.
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          3. User Responsibilities
        </Typography>
        <Typography variant="body1" paragraph>
          Users agree to:
          - Use the service for legitimate educational purposes
          - Not attempt to manipulate or abuse the system
          - Not use the service for cheating or academic dishonesty
          - Respect intellectual property rights
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          4. Limitations of Liability
        </Typography>
        <Typography variant="body1" paragraph>
          NuAnswers and its operators shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of or inability to use the service.
        </Typography>

        <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
          5. Contact Information
        </Typography>
        <Typography variant="body1" paragraph>
          For any questions about these Terms of Service, please contact us at:
          support@nuanswers.org
        </Typography>

        <Typography variant="body2" sx={{ mt: 4, color: 'text.secondary' }}>
          These terms of service constitute the entire agreement between you and NuAnswers regarding the use of our service.
        </Typography>
      </Paper>
    </Container>
  );
};

export default TermsOfService; 